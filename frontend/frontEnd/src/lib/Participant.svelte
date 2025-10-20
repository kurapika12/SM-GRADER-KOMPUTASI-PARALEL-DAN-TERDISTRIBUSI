<script>
  import { onMount } from 'svelte';

  let participants = [];
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
        correct: p.answers?.correct ?? 0,
        wrong: p.answers?.wrong ?? 0
      }));
      // keep original order copy
      originalParticipants = participants.slice();
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
          <p><strong>ID:</strong> {p.id}</p>
          <p><strong>Skor:</strong> {p.score}</p>
          <p><strong>Jawaban Benar:</strong> {p.correct}</p>
          <p><strong>Jawaban Salah:</strong> {p.wrong}</p>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .participants-container {
    margin: 2rem auto;
    max-width: 700px;
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
    width: 200px;
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
