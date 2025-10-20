<script>
  import { onMount } from 'svelte';
  
  let participantId = '';
  let loading = false;
  let error = '';
  let participant = null;

  async function fetchParticipant() {
    if (!participantId) {
      error = 'Masukkan ID peserta';
      return;
    }

    loading = true;
    error = '';
    
    try {
      // Gunakan endpoint getAnswerParticipant untuk mendapatkan semua data
      const response = await fetch('/getAnswerParticipant');
      if (!response.ok) throw new Error('Gagal mengambil data');
      
      const participants = await response.json();
      
      // Cari participant berdasarkan ID
      participant = participants.find(p => p.id === participantId);
      
      if (!participant) {
        error = 'Peserta tidak ditemukan';
        participant = null;
      }
    } catch (err) {
      error = err.message;
      participant = null;
    } finally {
      loading = false;
    }
  }
</script>

<div class="container">
  <h2>Halaman Peserta</h2>
  
  <div class="input-group">
    <label>
      ID Peserta:
      <input 
        bind:value={participantId}
        placeholder="Masukkan ID peserta"
      />
    </label>
    <button on:click={fetchParticipant}>
      Cari Data
    </button>
  </div>

  {#if loading}
    <p>Loading...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if participant}
    <div class="result">
      <h3>Data Peserta:</h3>
      <p><strong>ID:</strong> {participant.id}</p>
      <p><strong>Nama:</strong> {participant.name}</p>
      <p><strong>Nilai:</strong> {participant.score}</p>
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 1rem;
  }
  .input-group {
    margin: 1rem 0;
  }
  input {
    margin: 0 1rem;
    padding: 0.5rem;
  }
  button {
    padding: 0.5rem 1rem;
  }
  .error {
    color: red;
  }
  .result {
    margin-top: 2rem;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
</style>