<script>
  import svelteLogo from './assets/svelte.svg';
  import viteLogo from '/vite.svg';
  import Participant from './lib/Participant.svelte';

  let currentUser = null;
  let userIdInput = '';
  let errorMsg = '';
  let view = 'home';

  // Data dummy
  const users = [
    { id: "001", name: "ALAM", role: "user", score: 80, answers: { correct: 16, wrong: 4 } },
    { id: "002", name: "REYNALDO", role: "user", score: 90, answers: { correct: 18, wrong: 2 } },
    { id: "admin", name: "ADMIN PANEL", role: "admin", score: 0, answers: { correct: 0, wrong: 0 } }
  ];

  // Fungsi login
  function handleLogin() {
    const found = users.find(u => u.id === userIdInput.trim().toLowerCase());
    if (found) {
      currentUser = found;
      errorMsg = '';
      // Kalau admin langsung tampil halaman peserta
      view = currentUser.role === 'admin' ? 'participant' : 'home';
    } else {
      errorMsg = '❌ ID tidak ditemukan! ';
    }
  }

  // Fungsi logout
  function handleLogout() {
    currentUser = null;
    userIdInput = '';
    view = 'home';
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
    {/if}

    <!-- Halaman peserta untuk admin -->
    {#if view === 'participant' && currentUser.role === 'admin'}
      <h1 class="title">Halaman Peserta</h1>
      <div class="card">
        <Participant />
      </div>
    {/if}
  {/if}
</main>

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
  nav button.selected { background: rgba(255, 255, 255, 0.5); color: #1a1a1a; }
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
</style>
