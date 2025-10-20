<script>
  import svelteLogo from './assets/svelte.svg';
  import viteLogo from '/vite.svg';
  import Participant from './lib/Participant.svelte';
  
  let currentUser = null;
  let userIdInput = '';
  let errorMsg = '';
  let view = 'home';

  // Fungsi login: akan cek ke backend /api/grade?participantId=ID
  // Tetap sediakan akses 'admin' lokal supaya admin bisa melihat halaman peserta
  async function handleLogin() {
    const id = userIdInput.trim();
    if (!id) {
      errorMsg = 'Masukkan ID terlebih dahulu';
      return;
    }

    // Special-case admin (tidak disimpan di backend dummy)
    if (id.toLowerCase() === 'admin') {
      currentUser = { id: 'admin', name: 'ADMIN PANEL', role: 'admin', score: 0, answers: { correct: 0, wrong: 0 } };
      errorMsg = '';
      view = 'participant';
      return;
    }

    try {
      const res = await fetch(`http://localhost:3000/api/grade?participantId=${encodeURIComponent(id)}`);
      if (!res.ok) {
        if (res.status === 404) {
          errorMsg = '❌ ID tidak ditemukan!';
        } else {
          errorMsg = `Gagal mengambil data: ${res.status} ${res.statusText}`;
        }
        return;
      }

      const data = await res.json();
        // Normalisasikan struktur yang datang dari backend:
        // backend returns `answers` (full map) and `answersSummary` (correct/wrong), plus `score` and `lulus`.
        const normalized = {
          id: data.id || data._id || id,
          name: data.name || data.nama || 'Peserta',
          score: Number(data.score) || 0,
          answers: {
            correct: Number(data.answersSummary?.correct ?? data.answers?.correct ?? 0),
            wrong: Number(data.answersSummary?.wrong ?? data.answers?.wrong ?? 0)
          },
          lulus: Boolean(data.lulus),
          _answers: data.answers || {}
        };
        currentUser = { ...normalized, role: 'user' };
      errorMsg = '';
      view = 'home';
    } catch (e) {
      console.error(e);
      errorMsg = 'Gagal koneksi ke server. Pastikan backend berjalan di http://localhost:3000';
    }
  }

  // Fungsi logout
  function handleLogout() {
    currentUser = null;
    userIdInput = '';
    view = 'home';
  }

  // small helper: fetch question bank for user detail view
  let questionBank = [];

  async function ensureQuestionBank() {
    if (questionBank.length > 0) return;
    try {
      const res = await fetch('http://localhost:3000/questionBank');
      if (!res.ok) return;
      questionBank = await res.json();
    } catch (e) {
      console.warn('Failed to load question bank for user detail', e);
    }
  }

  function rightAnswerMap() {
    const m = {};
    for (const q of questionBank || []) {
      if (q && (q.questId || q.quest_id)) m[q.questId || q.quest_id] = q.rightAnswer || q.right_answer;
    }
    return m;
  }
</script>

<!-- Navbar -->
{#if currentUser}
  <nav class="nav-buttons">
    <!-- Hanya tampilkan tombol Logout untuk semua user -->
    <button class="logout" on:click={handleLogout}>Logout</button>
  </nav>
{/if}

<main>
  <!-- Logo & Login -->
  {#if !currentUser}
    <div class="logo-container">
      <img src={viteLogo} class="logo" alt="Vite Logo" />
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </div>

    <div class="login-box">
      <h1>Login</h1>
      <input
        type="text"
        placeholder="Masukkan ID"
        bind:value={userIdInput}
        on:keydown={(e) => e.key === 'Enter' && handleLogin()}
      />
      <button on:click={handleLogin}>Login</button>
      {#if errorMsg}
        <p class="error">{errorMsg}</p>
      {/if}
    </div>

  {:else}
    <!-- Dashboard user biasa -->
    {#if view === 'home' && currentUser.role !== 'admin'}
      <h1 class="title">Dashboard {currentUser.name}</h1>
      <!-- Pass/Fail badge for the current user -->
      <div class="user-status">
        {#if currentUser.lulus}
          <div class="status-badge pass">LULUS</div>
        {:else}
          <div class="status-badge fail">TIDAK LULUS</div>
        {/if}
      </div>
      <div class="dashboard">
        <div class="stat-card correct">
          <h2>{currentUser.answers.correct}</h2>
          <p>Jawaban Benar</p>
        </div>
        <div class="stat-card wrong">
          <h2>{currentUser.answers.wrong}</h2>
          <p>Jawaban Salah</p>
        </div>
        <div class="stat-card score">
          <h2>{currentUser.score}</h2>
          <p>Skor Akhir</p>
        </div>
      </div>
      <div class="user-detail-wrap">
        <button class="detail-btn" on:click={async () => { currentUser._showDetails = !currentUser._showDetails; if (currentUser._showDetails) await ensureQuestionBank(); }}>
          {currentUser._showDetails ? 'Sembunyikan Detail' : 'Lihat Detail' }
        </button>
        {#if currentUser._showDetails}
          <div class="detail-panel">
            {#if questionBank.length === 0}
              <p class="muted">Detail soal tidak tersedia — question bank belum dimuat.</p>
            {:else}
              <div class="q-list">
                {#each Object.keys(currentUser._answers || {}) as qid}
                  <div class="q-row { (rightAnswerMap()[qid] !== undefined && String(currentUser._answers[qid]) !== String(rightAnswerMap()[qid])) ? 'wrong' : 'correct' }">
                    <div class="q-id">{qid}</div>
                    <div class="q-right">Benar: {rightAnswerMap()[qid] ?? '-'}</div>
                    <div class="q-your">Jawaban: {currentUser._answers[qid] ?? '-'}</div>
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        {/if}
      </div>
    {/if}

    <!-- Halaman peserta untuk admin -->
    {#if view === 'participant' && currentUser.role === 'admin'}
      <h1 class="title">Halaman Peserta</h1>
      <div class="admin-panel">
        <Participant />
      </div>
    {/if}
  {/if}
</main>

<!-- Geometry Dash style cube orbiting the main container -->
<div class="cube-orbit" aria-hidden="true">
  <div class="orbiter orbiter-1">
    <svg class="cube cube-1" viewBox="0 0 200 200" width="110" height="110" xmlns="http://www.w3.org/2000/svg">
      <g>
        <rect x="40" y="40" width="120" height="120" rx="8" fill="#00bcd4" />
        <rect x="40" y="88" width="120" height="16" fill="#007c91" opacity="0.9" />
        <circle cx="88" cy="88" r="6" fill="#fff" />
        <circle cx="112" cy="88" r="6" fill="#fff" />
        <rect x="84" y="108" width="32" height="8" rx="4" fill="#ff6b6b" />
      </g>
    </svg>
  </div>

  <div class="orbiter orbiter-2">
    <svg class="cube cube-2" viewBox="0 0 200 200" width="90" height="90" xmlns="http://www.w3.org/2000/svg">
      <g>
        <rect x="40" y="40" width="120" height="120" rx="8" fill="#ff6f61" />
        <rect x="40" y="88" width="120" height="16" fill="#cc4b3f" opacity="0.95" />
        <circle cx="88" cy="88" r="6" fill="#fff" />
        <circle cx="112" cy="88" r="6" fill="#fff" />
        <rect x="84" y="108" width="32" height="8" rx="4" fill="#4a90e2" />
      </g>
    </svg>
  </div>

  <div class="orbiter orbiter-3">
    <svg class="cube cube-3" viewBox="0 0 200 200" width="70" height="70" xmlns="http://www.w3.org/2000/svg">
      <g>
        <rect x="40" y="40" width="120" height="120" rx="8" fill="#8e44ad" />
        <rect x="40" y="88" width="120" height="16" fill="#6a2a8f" opacity="0.95" />
        <circle cx="88" cy="88" r="6" fill="#fff" />
        <circle cx="112" cy="88" r="6" fill="#fff" />
        <rect x="84" y="108" width="32" height="8" rx="4" fill="#f1c40f" />
      </g>
    </svg>
  </div>
</div>

<style>
  :global(body) {
  margin: 0;
  font-family: 'Poppins', system-ui, sans-serif;
  background: url('./assets/text.jpg') no-repeat center center fixed;
  background-size: cover;
  color: #000000;
  display: flex;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
  padding: 2rem;
}


  nav.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 1.2rem;
    margin-bottom: 2rem;
    background: rgba(255, 255, 255, 0.15);
    padding: 1rem 2rem;
    border-radius: 14px;
    backdrop-filter: blur(10px);
  }

  nav button {
    padding: 0.7em 1.3em;
    font-size: 1em;
    font-weight: 500;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
    transition: transform 0.2s, background 0.3s;
  }

  nav button:hover { transform: translateY(-2px); background: rgba(255, 255, 255, 0.35); }
  .logout { background: #f44336; color: white; font-weight: 600; }
  .logout:hover { background: #d32f2f; }

  .logo-container { display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; }
  .logo { height: 6em; transition: transform 0.3s, filter 0.3s; cursor: pointer; }
  .logo:hover { transform: scale(1.1); filter: drop-shadow(0 0 20px #ffffffaa); }
  .logo.svelte:hover { filter: drop-shadow(0 0 20px #ff3e00aa); }

  .login-box {
    background: rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2rem;
    width: 350px;
    margin: 3rem auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    backdrop-filter: blur(15px);
  }

  .login-box input {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: none;
    margin: 10px 0;
    text-align: center;
  }

  .login-box button {
    background: #00C897;
    border: none;
    color: rgb(255, 255, 255);
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    width: 100%;
  }

  .login-box button:hover { background: #03b383; }

  .error { color: #ffcdd2; font-size: 0.9rem; margin-top: 10px; }

  .dashboard { display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 2rem; }

  .stat-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    padding: 2rem;
    border-radius: 20px;
    width: 200px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .stat-card:hover { transform: translateY(-6px); box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6); }
  .stat-card h2 { font-size: 3rem; margin: 0 0 0.5rem 0; }
  .stat-card.correct { border-top: 4px solid #4caf50; }
  .stat-card.wrong { border-top: 4px solid #f44336; }
  .stat-card.score { border-top: 4px solid #ff9800; }

  .title { font-size: 2rem; margin-bottom: 1rem; }

  .user-status { display:flex; justify-content:center; margin-bottom: 1rem; }
  .status-badge { padding: 0.5rem 1rem; border-radius: 999px; font-weight: 800; color: white; font-size: 0.95rem; }
  .status-badge.pass { background: #4caf50; }
  .status-badge.fail { background: #f44336; }

  /* Ensure main content sits above the background animation */
  main { position: relative; z-index: 1; }

  /* user detail styling (reuse Participant styles) */
  .user-detail-wrap { margin: 1rem auto; max-width: 760px; text-align: left; }
  .user-detail-wrap .detail-btn { background: #2196f3; color: white; border: none; padding: 0.45rem 0.8rem; border-radius: 8px; cursor: pointer; font-weight: 600; }
  .user-detail-wrap .detail-panel { margin-top: 0.8rem; max-height: 320px; overflow: auto; padding-right: 0.4rem; }
  .user-detail-wrap .q-list { display: grid; gap: 0.5rem; }
  .user-detail-wrap .q-row { display:flex; gap:0.6rem; align-items:center; padding:0.45rem; border-radius:8px; }
  .user-detail-wrap .q-row.correct { background: rgba(76,175,80,0.06); }
  .user-detail-wrap .q-row.wrong { background: rgba(244,67,54,0.06); }
  .user-detail-wrap .q-id { width: 60px; font-weight:700; }
  .user-detail-wrap .q-right { width: 120px; }

  /* admin panel sizing tweaks */
  .admin-panel { max-width: 1100px; margin: 0 auto; padding: 1rem; }

  /* Cube orbit animation (Geometry Dash style) */
  .cube-orbit { position: fixed; inset: 0; z-index: 0; pointer-events: none; }
  .orbiter {
    position: absolute;
    top: 50%;
    left: 50%;
    transform-origin: 50% 50%;
  }

  /* different orbit radii and speeds */
  .orbiter-1 { width: 220px; height: 220px; animation: orbit1 11s linear infinite; }
  .orbiter-2 { width: 320px; height: 320px; animation: orbit2 16s linear infinite reverse; }
  .orbiter-3 { width: 420px; height: 420px; animation: orbit3 22s linear infinite; }

  .cube { position: absolute; left: 100%; top: 50%; transform: translate(-50%, -50%); filter: drop-shadow(0 8px 10px rgba(0,0,0,0.18)); }

  .cube-1 { animation: cube-tilt-1 0.9s linear infinite; }
  .cube-2 { animation: cube-tilt-2 1.1s linear infinite; }
  .cube-3 { animation: cube-tilt-3 0.7s linear infinite; }

  @keyframes orbit1 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  @keyframes orbit2 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  @keyframes orbit3 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

  /* cube tilt/rotate to simulate dynamic motion */
  @keyframes cube-tilt-1 { 0% { transform: translate(-50%, -50%) rotate(0deg);} 50% { transform: translate(-50%, -50%) rotate(18deg);} 100% { transform: translate(-50%, -50%) rotate(0deg);} }
  @keyframes cube-tilt-2 { 0% { transform: translate(-50%, -50%) rotate(0deg);} 50% { transform: translate(-50%, -50%) rotate(-18deg);} 100% { transform: translate(-50%, -50%) rotate(0deg);} }
  @keyframes cube-tilt-3 { 0% { transform: translate(-50%, -50%) rotate(0deg);} 50% { transform: translate(-50%, -50%) rotate(28deg);} 100% { transform: translate(-50%, -50%) rotate(0deg);} }
</style>
