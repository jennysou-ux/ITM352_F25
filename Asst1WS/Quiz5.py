# Improved quiz game with questions and answers in a dictionary.
# Iterate until the user enters a correct alternative.
# Keep track of correct answers.
# Name: Rick Kazman
# Date: 10/2/25

from string import ascii_letters

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "11", "15", "8"],
    "What is the capital of Texas": ["Austin", "Dallas", "Houston", "San Antonio"],
    "The Last Supper was painted by which artist": ["Da Vinci", "Michelangelo", "Raphael", "Donatello"]
}

num_correct = 0

for qnum, (question, answers) in enumerate(QUESTIONS.items(), start=1):
    print(f"Question {qnum}:")
    print(f"{question}? ")
    correct_answer = answers[0]  # By convention, the first answer in the list is the correct one.
    labelled_answers = dict(zip(ascii_letters, sorted(answers)))  # Create a dictionary of labelled answers.

    for label, answer in labelled_answers.items():  # Add a letter to each possible answer.
        print(f"{label}. {answer}")

    answer_label = input(f"\nChoice? ")  # Get the user's answer as a label.
    answer = labelled_answers.get(answer_label)  # Get the user's answer from the labelled list.

    if answer == correct_answer:  # Compare the user's answer to the correct answer.
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")

print(f"\nYou got {num_correct} out of {len(QUESTIONS)} questions correct.")