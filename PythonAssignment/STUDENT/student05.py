"""
Module: student05.py
Description: Allows students to submit feedback.
"""

from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def get_list(file_path, num):
    """
    Retrieves a unique list of values from a specified column in a CSV file.
    Skips the header and returns a list of unique entries.
    """
    subjects = set()
    with open(file_path, "r") as file:
        next(file)  # Skip header line.
        for line in file:
            subject = line.strip().split(",")[num]
            subjects.add(subject)
    return list(subjects)


def submit_feedback(user):
    """
    Allows a student to submit feedback.
    Prompts the student for a receiver, a rating (between 1 and 5), and a comment,
    then appends the feedback to the designated feedback file.
    """
    # Display header for feedback submission.
    print_separator("Feedback Submission")

    while True:
        # Prompt the student for feedback-related actions.
        user_choices = prompt("Choose your choices", ["Submit Feedback", "Quit"])

        if user_choices == "Quit":
            break

        elif user_choices == "Submit Feedback":
            print_separator("Submit Feedback")
            file_path = "../DATA/feedback.txt"
            student_id = user["TP_number"]

            # Get a list of potential receivers from the user file.
            receiver_list = get_list("../DATA/user.txt", 0)
            receiver = prompt(f"Which is your receiver？ ", receiver_list)

            # Continuously prompt until a valid rating is entered.
            while True:
                rating = input("Rate the course (1-5): ").strip()
                if rating.isdigit() and 1 <= int(rating) <= 5:
                    break
                else:
                    print("Invalid rating. Please enter a number between 1 and 5.")

            # Get feedback comment from the student.
            comment = input("Enter your feedback: ").strip()

            # Prepare the feedback data.
            feedback_list = []
            feedback_dict = {
                "TP_number": student_id,
                "Receiver": receiver,
                "Rating": rating,
                "Comment": comment,
            }
            feedback_list.append(feedback_dict)
            data = feedback_list

            if not data:
                return

            # Append the feedback to the feedback file.
            with open(file_path, "a") as file:
                for row in data:
                    file.write("\n" + ",".join(str(value) for value in row.values()))
