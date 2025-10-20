from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'dummy_participant.json')
QUESTION_BANK = os.path.join(os.path.dirname(__file__), 'question_bank.json')
QUESTION_DUMMY = os.path.join(os.path.dirname(__file__), 'question_dummy.json')


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


def load_question_bank():
    try:
        with open(QUESTION_BANK, 'r') as f:
            qlist = json.load(f)
        # convert to map questId -> rightAnswer
        qmap = {}
        for q in qlist:
            if isinstance(q, dict):
                qid = q.get('questId') or q.get('quest_id')
                right = q.get('rightAnswer') or q.get('rightAnswer'.lower())
                if qid and right:
                    qmap[str(qid)] = right
        return qmap
    except Exception:
        return {}


def grade_participant_answers(answers, question_map):
    # answers: dict mapping questionId -> answer
    correct = 0
    wrong = 0
    for qid, right in question_map.items():
        user_ans = answers.get(qid)
        if user_ans is None:
            # skip unanswered
            continue
        if str(user_ans) == str(right):
            correct += 1
        else:
            wrong += 1
    score = compute_score_from_answers({'correct': correct, 'wrong': wrong})
    return { 'correct': correct, 'wrong': wrong, 'score': score, 'lulus': True if score >= 60 else False }

# === [GET] Ambil data peserta dari file dummy ===
@app.route('/getAnswerParticipant', methods=['GET'])
def get_answer_participant():
    try:
        # load question bank and participants
        qmap = load_question_bank()
        with open(QUESTION_DUMMY, 'r') as f:
            participants = json.load(f)

        graded = []
        for p in participants:
            ans = p.get('answers') or {}
            res = grade_participant_answers(ans, qmap)
            graded.append({
                'id': p.get('_id') or p.get('noUjian') or p.get('id'),
                'name': p.get('name'),
                'answers': ans,
                'score': res['score'],
                'answersSummary': { 'correct': res['correct'], 'wrong': res['wrong'] },
                'lulus': res['lulus']
            })
        return jsonify(graded)
    except Exception as e:
        return jsonify({"error": f"Gagal membaca data peserta: {str(e)}"}), 500

# === [GET] Ambil nilai peserta berdasarkan ID ===
@app.route('/api/grade', methods=['GET'])
def get_participant_grade():
    participant_id = request.args.get('participantId')
    if not participant_id:
        return jsonify({"error": "Parameter participantId diperlukan"}), 400
    
    try:
        qmap = load_question_bank()
        with open(QUESTION_DUMMY, 'r') as f:
            participants = json.load(f)

        participant = next((p for p in participants if str(p.get('_id')) == str(participant_id) or str(p.get('noUjian')) == str(participant_id) or str(p.get('id')) == str(participant_id)), None)
        if not participant:
            return jsonify({"error": f"Peserta dengan ID {participant_id} tidak ditemukan"}), 404

        res = grade_participant_answers(participant.get('answers') or {}, qmap)
        participant_out = {
            'id': participant.get('_id') or participant.get('noUjian') or participant.get('id'),
            'name': participant.get('name'),
            'answers': participant.get('answers') or {},
            'score': res['score'],
            'answersSummary': { 'correct': res['correct'], 'wrong': res['wrong'] },
            'lulus': res['lulus']
        }
        return jsonify(participant_out)
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


# === [GET] Return question bank ===
@app.route('/questionBank', methods=['GET'])
def get_question_bank():
    try:
        with open(QUESTION_BANK, 'r') as f:
            qlist = json.load(f)
        return jsonify(qlist)
    except Exception as e:
        return jsonify({"error": f"Gagal membaca question bank: {str(e)}"}), 500

# === Root endpoint ===
@app.route('/')
def home():
    return jsonify({"message": "SM Grader Flask API is running 🚀"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)