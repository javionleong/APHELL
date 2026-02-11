"""
Module: student01.py
Description: Contains functions for managing student account details, including viewing and updating details and financial information.
"""

from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def update_details(user):
    """
    Allows a student to view and update their account details.
    Validates the student's login and provides options to show details, update details, or view financial information.
    """
    # Define the file path for student details and read the data.
    file_path = "../DATA/studentdetail.txt"
    student_details = read(file_path)

    # Find the matching student record based on TP_number and Password.
    detail = None
    for detail_item in student_details:
        if (
            detail_item["TP_number"] == user["TP_number"]
            and detail_item["Password"] == user["Password"]
        ):
            detail = detail_item
            break
    else:
        # If no match is found, inform the user and exit.
        print("Invalid TP Number or Password")
        return

    # Display header for the Student Account Management section.
    print_separator("Student Account Management")

    while True:
        # Present options for account management.
        user_choices = prompt(
            "Choose your choices",
            ["Show Details", "Update Details", "View Financial", "Quit"],
        )

        if user_choices == "Quit":
            break

        elif user_choices == "Show Details":
            # Show the student's details.
            print_separator("Show Details")
            if detail:
                students = read(file_path)
                student_list = []
                for student in students:
                    if student["TP_number"] == user["TP_number"]:
                        student_list.append(student)
                        data = student_list
                        selected_table(data)

        elif user_choices == "Update Details":
            # Process updating of student details.
            entity_type = "student"
            id_field = "TP_number"
            data_path = "../DATA/studentdetail"

            print_separator("Update Details")
            entity_id = user["TP_number"]
            if entity_id.upper() == "QUIT":
                return

            # Retrieve the student record for updating.
            row = get_row(data_path, id_field, entity_id)
            if not row:
                print(f"{entity_type} with {id_field} {entity_id} not found!")
                return

            # Display the current details.
            print(f"{entity_type} found: ", end="")
            for key, value in row.items():
                print(f"{key}: {value}", end=", ")
            print()

            # Specify the fields that can be updated.
            allowed_fields = [
                "Password",
                "Contact",
                "Address",
                "Emergency_contact",
                "Emergency_relationship",
            ]
            update = prompt("Select field to update:", allowed_fields + ["QUIT"])
            if update.upper() == "QUIT":
                return

            # Get new value from the user.
            new_value = input(f"Enter new {update} (or 'QUIT' to cancel): ")
            if new_value.upper() == "QUIT":
                return

            # If updating the password, update in the user file as well.
            if update == "Password":
                update_row("../DATA/user", id_field, entity_id, update, new_value)

            # Update the student details.
            update_row(data_path, id_field, entity_id, update, new_value)
            print(
                f"{entity_type} {entity_id} updated successfully! {update} changed to {new_value}"
            )

        elif user_choices == "View Financial":
            # Retrieve and display financial details for the student.
            financial_list = []
            reader = read("../DATA/financial.txt")
            for line in reader:
                if user["TP_number"] == line["TP_number"]:
                    financial_list.append(line)
            data = financial_list
            selected_table(data)
