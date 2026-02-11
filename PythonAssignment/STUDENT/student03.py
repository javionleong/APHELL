"""
Module: student03.py
Description: Provides functionality for accessing course materials based on the student's enrolled course.
"""

from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def material_access(user):
    """
    Allows students to access course materials.
    Filters subjects based on the student's enrolled course and displays available materials.
    """
    # Read student details to validate the login and determine the enrolled course.
    valid_login = read("../DATA/studentdetail.txt")

    # Display header for course material access.
    print_separator("Course Material Access")

    while True:
        # Prompt the user for material access options.
        user_choices = prompt("Choose your choices", ["View Materials", "Quit"])

        if user_choices == "Quit":
            break

        elif user_choices == "View Materials":
            print_separator("View Materials")
            file_path = "../DATA/subject_data.txt"
            unique_subjects = []
            seen_subjects = set()

            # Determine the target course from the student's details.
            for line in valid_login:
                if user["TP_number"] == line["TP_number"]:
                    target_course = line["Course_id"]

            # Open the subject data file and collect unique subjects for the target course.
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) < 2:
                        continue
                    course_id, subject_name = parts[0], parts[1]
                    if course_id == target_course and subject_name not in seen_subjects:
                        unique_subjects.append(subject_name)
                        seen_subjects.add(subject_name)

            # Prompt the student to select a subject.
            class_choice = prompt("Which subject do you want to view?", unique_subjects)

            # Validate the subject choice and display corresponding materials.
            if class_choice.lower() in (subject.lower() for subject in unique_subjects):
                with open(file_path, "r") as file:
                    for line in file:
                        parts = line.strip().split(",")
                        if len(parts) < 2:
                            continue
                        course_id, subject, material_type, link = line.strip().split(
                            ","
                        )
                        if subject.lower() == class_choice.lower():
                            print(f"Material Type: {material_type}, Link: {link}")
            else:
                print("Invalid subject choice!")
