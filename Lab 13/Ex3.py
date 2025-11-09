# Lab 13 Exercise 3 Meme Viewer and Quiz Game
# Author: Jenny Soukhaseum 

from flask import Flask, render_template, session, redirect, url_for, request, flash
import requests
import logging
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

MEME_API_URL = "https://meme-api.com/gimme/wholesomememes"

def fetch_meme(timeout: float = 5.0):
    try:
        resp = requests.request("GET", MEME_API_URL, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        meme_url = data.get("url")
        subreddit = data.get("subreddit", "unknown")
        title = data.get("title", "")
        if not meme_url:
            raise RuntimeError("No image URL returned by meme API")
        return meme_url, subreddit, title
    except Exception as e:
        raise RuntimeError(f"Failed to fetch meme: {e}")

@app.route("/")
def home():
    try:
        meme_url, subreddit, title = fetch_meme()
        return render_template("memes.html", meme_url=meme_url, subreddit=subreddit, title=title, error_message=None)
    except RuntimeError as e:
        return render_template("memes.html", meme_url=None, subreddit=None, title=None, error_message=str(e))

# Simple quiz skeleton
QUIZ_QUESTIONS = [
    {"q": "What color is the sky on a clear day?", "choices": ["Blue", "Green", "Red"], "answer": 0},
    {"q": "2 + 2 = ?", "choices": ["3", "4", "5"], "answer": 1},
]

def init_quiz():
    session["q_index"] = 0
    session["score"] = 0

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "q_index" not in session:
        init_quiz()

    if request.method == "POST":
        choice = request.form.get("choice")
        try:
            choice = int(choice)
        except (TypeError, ValueError):
            choice = None
        idx = session.get("q_index", 0)
        if 0 <= idx < len(QUIZ_QUESTIONS) and choice is not None:
            if choice == QUIZ_QUESTIONS[idx]["answer"]:
                session["score"] = session.get("score", 0) + 1
                flash("Correct!", "info")
            else:
                flash("Incorrect.", "info")
            session["q_index"] = idx + 1
        return redirect(url_for("quiz"))

    idx = session.get("q_index", 0)
    if idx >= len(QUIZ_QUESTIONS):
        score = session.get("score", 0)
        total = len(QUIZ_QUESTIONS)
        return render_template("quiz.html", finished=True, score=score, total=total)
    q = QUIZ_QUESTIONS[idx]
    return render_template("quiz.html", finished=False, question=q["q"], choices=q["choices"], index=idx+1, total=len(QUIZ_QUESTIONS))

@app.route("/quiz/reset")
def quiz_reset():
    init_quiz()
    flash("Quiz reset.", "info")
    return redirect(url_for("quiz"))

if __name__ == "__main__":
    app.run(debug=True)