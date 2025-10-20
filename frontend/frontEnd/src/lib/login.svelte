<script>
  import { createEventDispatcher, onMount } from 'svelte';
  const dispatch = createEventDispatcher();

  let id = '';
  let error = '';
  let loading = false;
  let participants = [];

  // Ambil data peserta dari backend saat komponen dimount
  onMount(async () => {
    loading = true;
    error = '';
    try {
      const res = await fetch('http://localhost:3000/getAnswerParticipant');
      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText}`);
      }
      participants = await res.json();
    } catch (e) {
      console.error('Gagal mengambil daftar peserta:', e);
      error = 'Gagal mengambil data peserta. Pastikan backend berjalan di http://localhost:3000';
    } finally {
      loading = false;
    }
  });

  function handleLogin() {
    const lookupId = id.trim();
    if (!lookupId) {
      error = 'Masukkan ID terlebih dahulu.';
      return;
    }

    // Cari di data peserta yang diambil dari backend
    const user = participants.find(u => String(u.id) === String(lookupId));
    if (user) {
      // Normalisasikan objek user supaya konsisten dengan penggunaan di app
      const payload = {
        id: String(user.id),
        name: user.name || user.nama || 'Peserta',
        score: user.score ?? 0,
        answers: user.answers ?? { correct: 0, wrong: 0 },
        role: 'user'
      };
      dispatch('loginSuccess', { user: payload });
      error = '';
    } else {
      error = 'ID tidak ditemukan. Coba lagi.';
    }
  }
</script>

<div class="login-container">
  <h1>Login</h1>
  <input
    type="text"
    placeholder="Masukkan ID Anda (contoh: 001)"
    bind:value={id}
  />
  <button on:click={handleLogin}>Masuk</button>

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>

<style src="./Login.css"></style>
