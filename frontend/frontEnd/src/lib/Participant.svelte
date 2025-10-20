<script>
  // Data peserta yang langsung tampil untuk admin
  const participants = [
    { id: "001", name: "ALAM", score: 80, correct: 16, wrong: 4 },
    { id: "002", name: "REYNALDO", score: 90, correct: 18, wrong: 2 }
  ];
</script>

<div class="participants-container">
  <h2>Data Peserta</h2>
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
</style>
