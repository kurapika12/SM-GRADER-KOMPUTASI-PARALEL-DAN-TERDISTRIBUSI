from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'dummy_participant.json')


def compute_score_from_answers(answers, fallback=0):
    """Compute percentage score from an answers object with keys 'correct' and 'wrong'.
    If no answers info available, return fallback.
    """
    try:
        if not answers:
            return fallback
        correct = int(answers.get('correct') or 0)
        wrong = int(answers.get('wrong') or 0)
    except Exception:
        return fallback
    total = correct + wrong
    if total > 0:
        return round((correct / total) * 100, 2)
    return fallback

# === [GET] Ambil data peserta dari file dummy ===
@app.route('/getAnswerParticipant', methods=['GET'])
def get_answer_participant():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)

        for p in data:
            p['score'] = compute_score_from_answers(p.get('answers'), p.get('score', 0))

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Gagal membaca data peserta: {str(e)}"}), 500

# === [GET] Ambil nilai peserta berdasarkan ID ===
@app.route('/api/grade', methods=['GET'])
def get_participant_grade():
    participant_id = request.args.get('participantId')
    if not participant_id:
        return jsonify({"error": "Parameter participantId diperlukan"}), 400
    
    try:
        with open(DATA_FILE, 'r') as file:
            participants = json.load(file)

        # Cari peserta berdasarkan ID
        participant = next((p for p in participants if str(p.get('id')) == str(participant_id)), None)
        if not participant:
            return jsonify({"error": f"Peserta dengan ID {participant_id} tidak ditemukan"}), 404

        # Hitung score berdasarkan answers (jika ada) menggunakan helper terpusat
        participant['score'] = compute_score_from_answers(participant.get('answers'), participant.get('score', 0))

        return jsonify(participant)
    except Exception as e:
        return jsonify({"error": f"Gagal membaca data: {str(e)}"}), 500

# === [POST] Hitung nilai otomatis ===
@app.route('/api/grade', methods=['POST'])
def calculate_grade():

    data = request.get_json()
    benar, total = 0, 0

    for section, section_data in data['summary']['groupBySection'].items():
        for qid, qdata in section_data['questions'].items():
            total += 1
            key = qdata['rightAnswers']
            ans = data['answers'].get(qid)
            if ans == key:
                benar += 1

    skor = round((benar / total) * 100, 2) if total > 0 else 0
    return jsonify({"score": skor, "total": total, "correct": benar})

# === Root endpoint ===
@app.route('/')
def home():
    return jsonify({"message": "SM Grader Flask API is running 🚀"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)