<script>
  import { onMount } from 'svelte';

  let participants = [];
  let questionBank = [];
  // keep a copy of the original order (as fetched) so initial state is "random"/unchanged
  let originalParticipants = [];
  let loading = true;
  let error = '';
  // whether the list has been sorted by score (descending)
  let sorted = false;

  // Ambil data peserta dari backend
  async function loadParticipants() {
    loading = true;
    error = '';
    try {
      const res = await fetch('http://localhost:3000/getAnswerParticipant');
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const data = await res.json();
      // Map ke format yang dipakai di tampilan
      participants = data.map(p => ({
        id: p.id,
        name: p.name,
        score: Number(p.score) || 0,
        correct: Number(p.answersSummary?.correct ?? p.answers?.correct ?? 0),
        wrong: Number(p.answersSummary?.wrong ?? p.answers?.wrong ?? 0),
        lulus: Boolean(p.lulus),
        _answers: p.answers || {}
      }));
      // keep original order copy
      originalParticipants = participants.slice();
      // also try to fetch question bank (non-blocking)
      try {
        const qb = await fetch('http://localhost:3000/questionBank');
        if (qb.ok) questionBank = await qb.json();
      } catch (e) {
        // ignore question bank errors here; details view will show fallback message
        console.warn('Failed to load question bank', e);
      }
    } catch (e) {
      console.error('Failed to load participants', e);
      error = 'Gagal memuat data peserta. Pastikan backend berjalan di http://localhost:3000';
    } finally {
      loading = false;
    }
  }

  function sortByScoreDescending() {
    participants = participants.slice().sort((a, b) => (Number(b.score) || 0) - (Number(a.score) || 0));
    sorted = true;
  }

  onMount(() => {
    loadParticipants();
  });

  function resetOrder() {
    participants = originalParticipants.slice();
    sorted = false;
  }

  // helper: build a quick map of right answers from questionBank for lookup
  function rightAnswerMap() {
    const m = {};
    for (const q of questionBank || []) {
      if (q && (q.questId || q.quest_id)) m[q.questId || q.quest_id] = q.rightAnswer || q.right_answer;
    }
    return m;
  }
</script>

<div class="participants-container">
  <h2>Data Peserta</h2>
  <div class="controls">
    {#if !loading && !error}
      {#if !sorted}
        <button class="sort-btn" on:click={sortByScoreDescending}>Sort by Skor (Tertinggi → Terendah)</button>
      {:else}
        <span class="sorted-badge">Terurut: Tertinggi → Terendah</span>
        <button class="reset-btn" on:click={resetOrder}>Reset Urutan</button>
      {/if}
    {/if}
  </div>
  {#if loading}
    <p>Memuat data peserta...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else}
    <div class="cards">
      {#each participants as p}
        <div class="card">
          <h3>{p.name}</h3>
          {#if p.lulus}
            <div class="lulus-badge">LULUS</div>
          {:else}
            <div class="lulus-badge fail">TIDAK LULUS</div>
          {/if}
          <p><strong>ID:</strong> {p.id}</p>
          <p><strong>Skor:</strong> {p.score}</p>
          <p><strong>Jawaban Benar:</strong> {p.correct}</p>
          <p><strong>Jawaban Salah:</strong> {p.wrong}</p>
          <button class="detail-btn" on:click={() => p._showDetails = !p._showDetails}>{p._showDetails ? 'Sembunyikan Detail' : 'Lihat Detail'}</button>
          {#if p._showDetails}
            <div class="detail-panel">
              {#if questionBank.length === 0}
                <p class="muted">Detail soal tidak tersedia — question bank belum dimuat.</p>
              {:else}
                {#if p.correct === 0}
                  <p class="muted">Peserta belum benar pada soal manapun.</p>
                {/if}
                <div class="q-list">
                  {#each Object.keys(p._answers || {}) as qid}
                    <div class="q-row { (rightAnswerMap()[qid] !== undefined && String(p._answers[qid]) !== String(rightAnswerMap()[qid])) ? 'wrong' : 'correct' }">
                      <div class="q-id">{qid}</div>
                      <div class="q-right">Benar: {rightAnswerMap()[qid] ?? '-'}</div>
                      <div class="q-your">Jawaban: {p._answers[qid] ?? '-'}</div>
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .participants-container {
    margin: 2rem auto;
    max-width: 980px;
    text-align: center;
  }

  .cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
  }

  .card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 15px;
    width: 240px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    color: #000000;
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
  }

  .card h3 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-size: 1.3rem;
  }

  .lulus-badge {
    display: inline-block;
    margin-bottom: 0.5rem;
    padding: 0.25rem 0.5rem;
    border-radius: 999px;
    background: #4caf50;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
  }
  .lulus-badge.fail { background: #f44336; }

  .detail-btn {
    margin-top: 0.6rem;
    background: #2196f3;
    color: white;
    border: none;
    padding: 0.35rem 0.6rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
  }

  .detail-panel { margin-top: 0.8rem; text-align: left; }
  .muted { color: rgba(0,0,0,0.5); font-style: italic; }
  .q-list { display: grid; gap: 0.5rem; margin-top: 0.6rem; }
  .q-row { display: flex; gap: 0.6rem; align-items: center; padding: 0.45rem; border-radius: 8px; flex-wrap: wrap; }
  .q-row.correct { background: rgba(76,175,80,0.08); }
  .q-row.wrong { background: rgba(244,67,54,0.08); }
  .q-id { font-weight: 700; width: 60px; }
  .q-right { color: #333; width: 120px; }
  .q-your { color: #111; font-weight: 600; }

  .card p {
    margin: 0.3rem 0;
    font-size: 0.95rem;
  }
  .controls {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }

  .sort-btn, .reset-btn {
    background: #00C897;
    color: #fff;
    border: none;
    padding: 0.5rem 0.9rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
  }

  .reset-btn {
    background: #f0ad4e;
  }

  .sort-btn:hover { filter: brightness(0.95); }
  .reset-btn:hover { filter: brightness(0.95); }

  .sorted-badge {
    display: inline-block;
    padding: 0.45rem 0.65rem;
    background: rgba(0,0,0,0.06);
    border-radius: 999px;
    font-weight: 600;
    align-self: center;
  }
</style>
