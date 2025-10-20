<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  let id = '';
  let error = '';

  // Data dummy user
  const users = [
    { id: '001', name: 'ALAM', score: 80, correct: 8, wrong: 2 },
    { id: '002', name: 'REYNALDO', score: 90, correct: 9, wrong: 1 }
  ];

  function handleLogin() {
    const user = users.find(u => u.id === id);
    if (user) {
      dispatch('loginSuccess', { user });
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
