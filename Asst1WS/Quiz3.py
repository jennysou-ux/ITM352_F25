# Quiz 3. Put questions and answers into a dictionary
# Incldue answer options
#  Name: Jenny Soukhaseum
# Date: 10/03/2025

# Quiz questions. For each question list the possible answers, with the first answer being the correct one.
QUESTIONS = [
    ("What is the airspeed of an unladen swallow in miles per hour ",  ["12", "24", "36"], "12"),
    ("What is the capital of Texas ", ["Austin", "Dallas", "Houston"], "Austin"),
    ("The last supper was painted by which famous artist ", ["Leonardo da Vinci", "Michelangelo", "Raphael"], "Leonardo da Vinci")
]

for question, alternatives in QUESTIONS.items():
    correct_answer = alternatives[0]
    for alternative in sorted(alternatives):
        print(f" - {alternative}")

answer = input(f"{question}")
if answer == correct_answer:
        print("Correct!")
else:
        print(f"The answer is {correct_answer}, not {answer}.")

  
