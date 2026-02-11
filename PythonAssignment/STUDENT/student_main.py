"""
Module: student_main.py
Description: Main entry point for the student module that handles user interaction and routes to various functionalities.
"""

# Import necessary functions and modules from other parts of the application.
from FUNCTION.view_everything import view_all
from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *
from STUDENT.student01 import *
from STUDENT.student02 import *
from STUDENT.student03 import *
from STUDENT.student04 import *
from STUDENT.student05 import *


def student_main(user):
    """
    Main function for the student interface.
    Presents a menu to the student and routes to the selected functionality.
    """
    while True:
        # Display the student menu header.
        print_separator("Student Menu")

        # Prompt the user to choose an option from the menu.
        user_choices = prompt(
            "Choose ur choices",
            [
                "Student Account Management",
                "Course Enrolment",
                "Course Material Access",
                "Grades Tracking",
                "Feedback Submission",
                "View All",
                "Quit",
            ],
        )

        # Check the user's choice and execute the corresponding functionality.
        if user_choices == "Quit":
            exit()
        elif user_choices == "Student Account Management":
            update_details(user)
        elif user_choices == "Course Enrolment":
            course_enrollment(user)
        elif user_choices == "Course Material Access":
            material_access(user)
        elif user_choices == "Grades Tracking":
            view_grade(user)
        elif user_choices == "Feedback Submission":
            submit_feedback(user)
        elif user_choices == "View All":
            view_all(user)
