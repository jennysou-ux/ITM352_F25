import json, random, os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for sessions

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(SCRIPT_DIR, "questions.json")
SCORES_FILE = os.path.join(SCRIPT_DIR, "scores.json")

# Helper Functions
def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    # Randomize question order and options
    random.shuffle(questions)
    for q in questions:
        items = list(q["options"].items())
        random.shuffle(items)
        q["options"] = dict(items)
    return questions

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

# --- Routes
@app.route("/")
def index():
    # Persistent user check
    if "username" in session:
        scores = load_scores()
        user_scores = [s for s in scores if s["name"] == session["username"]]
        return render_template("index.html", username=session["username"], history=user_scores)
    return render_template("index.html", username=None)

@app.route("/setname", methods=["POST"])
def setname():
    session["username"] = request.form["username"]
    return redirect(url_for("quiz"))

@app.route("/quiz")
def quiz():
    session["questions"] = load_questions()
    session["score"] = 0
    session["current"] = 0
    return render_template("quiz.html", question=session["questions"][0], qnum=1, total=len(session["questions"]))

@app.route("/answer", methods=["POST"])
def answer():
    choice = request.form["choice"]
    qnum = session["current"]
    question = session["questions"][qnum]

    if choice == question["answer"]:
        session["score"] += 1

    session["current"] += 1
    if session["current"] >= len(session["questions"]):
        return redirect(url_for("result"))
    else:
        next_q = session["questions"][session["current"]]
        return render_template("quiz.html", question=next_q, qnum=session["current"]+1, total=len(session["questions"]))

@app.route("/result")
def result():
    score = session["score"]
    total = len(session["questions"])
    scores = load_scores()
    scores.append({"name": session["username"], "score": score})
    save_scores(scores)

    return render_template("result.html", score=score, total=total)

@app.route("/leaderboard")
def leaderboard():
    scores = load_scores()
    scores.sort(key=lambda x: x["score"], reverse=True)
    top10 = scores[:10]
    return render_template("leaderboard.html", scores=top10)

if __name__ == "__main__":
    app.run(debug=True)