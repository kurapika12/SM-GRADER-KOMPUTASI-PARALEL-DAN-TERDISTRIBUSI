from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # biar bisa diakses dari frontend Svelte

DATA_FILE = os.path.join(os.path.dirname(__file__), 'dummy_participant.json')

# === [GET] Ambil data peserta dari file dummy ===
@app.route('/getAnswerParticipant', methods=['GET'])
def get_answer_participant():
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
    return jsonify(data)

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
