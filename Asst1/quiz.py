import json
import os
from datetime import datetime

# Get the directory where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths to your data files
QUESTIONS_FILE = os.path.join(SCRIPT_DIR, "questions.json")
SCORES_FILE    = os.path.join(SCRIPT_DIR, "scores.txt")

def load_questions(filepath):
    """Load quiz questions from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)



def get_valid_answer(options):
    """
    Prompt user until they enter one of the valid option keys.
    Returns the chosen key.
    """
    valid_keys = options.keys()
    while True:
        choice = input(f"Your answer ({'/'.join(valid_keys)}): ").strip().lower()
        if choice in valid_keys:
            return choice
        print("Invalid response. Please enter one of", ", ".join(valid_keys))


def read_high_score(filepath):
    """
    Read past scores and return the highest one.
    If file does not exist, return 0.
    """
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        scores = [int(line.split()[0]) for line in f if line.strip()]
    return max(scores) if scores else 0


def record_score(filepath, score):
    """
    Append the new score with timestamp to the history file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"{score} {timestamp}\n")


def run_quiz():
    """
    Main quiz loop: asks each question, checks answers, tracks score,
    records history, and notifies on a new high score.
    """
    questions = load_questions(QUESTIONS_FILE)
    score = 0
    total = len(questions)

    print(f"Welcome to the Trivia Quiz! You will be asked {total} questions.\n")

    for idx, q in enumerate(questions, start=1):
        print(f"Question {idx}: {q['question']}")
        for key, text in q["options"].items():
            print(f"  {key}) {text}")
        answer = get_valid_answer(q["options"])
        if answer == q["answer"]:
            print("Correct!\n")
            score += 1
        else:
            correct_text = q["options"][q["answer"]]
            print(f"Incorrect. The correct answer was ({q['answer']}) {correct_text}.\n")

    print(f"Quiz complete! Your final score is {score}/{total}.\n")

    high_score = read_high_score(SCORES_FILE)
    record_score(SCORES_FILE, score)

    if score > high_score:
        print("Congratulations! You achieved a new high score!\n")
    else:
        print(f"The current high score is {high_score}. Better luck next time!\n")


if __name__ == "__main__":
    run_quiz()