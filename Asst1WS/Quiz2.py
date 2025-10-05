# Quiz 2. Put questions and answers into a list 
# Name: Jenny Soukhaseum
# Date: 10/03/2025

QUESTIONS = [
    ("What is the airspeed of an unladen swallow in miles per hour ", "12"),
    ("What is the capital of Texas ", "Austin"),
    ("The last supper was painted by which famous artist ", "Leonardo da Vinci")
    ]

for question, correct_answer in QUESTIONS:
    answer = input(f"{question}")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is {correct_answer}, not {answer}.")

    