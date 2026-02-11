from COMMON.csv import *
from COMMON.prompt import *
from COMMON.design import *


def student_management():
    """Menu for managing student-related information."""
    while True:
        print_separator("STUDENT MANAGEMENT MENU")

        choice = prompt(
            "Select a category (enter 'QUIT' to quit):",
            [
                "Student Personal Details",
                "Student Enrollment Status",
                "Student Academic Performance",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print("\nBye bye, Admin.\n")
            break

        file_paths = {
            "Student Personal Details": "../DATA/studentdetail.txt",
            "Student Enrollment Status": "../DATA/enrolment.txt",
            "Student Academic Performance": "../DATA/grades.txt",
        }

        if choice not in file_paths:
            continue

        file_path = file_paths[choice]
        print_separator(choice)

        action = prompt(
            f"What would you like to do with {choice}?", ["View", "Update", "Back"]
        )

        try:
            if action == "View":
                table(file_path)  # Display the selected file as a table
            elif action == "Update":
                update_entity("TP_number", "TP_number", file_path.replace(".txt", ""))
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")

        if action == "Back":
            continue
