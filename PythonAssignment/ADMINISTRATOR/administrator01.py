from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def admin_menu():
    """Admin menu for managing users."""
    while True:
        print_separator("ADMIN MENU")

        # Prompt admin to select an option
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all users",
                "Add a new user",
                "Update user details",
                "Delete a user",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print_separator("\nBye bye, Admin\n")
            break

        # Display all users from user.txt
        if choice == "View all users":
            print_separator("Table of Users")
            table("../DATA/user.txt")

        elif choice == "Add a new user":
            print_separator("Adding a New User")

            # Load existing users and course details
            users = get_all_rows("../DATA/user")
            course_data = get_all_rows("../DATA/course")  # Load course data for fees

            # Prompt to select user role
            role = prompt(
                "Select Role:",
                ["Administration", "Student", "Teacher", "Staff", "QUIT"],
            )

            if role == "QUIT":
                continue

            # Role-based TP number prefix
            role_prefix = {
                "Administration": "A",
                "Student": "S",
                "Teacher": "T",
                "Staff": "STAFF",
            }

            # Generate new TP_number based on existing users
            numeric_tp_numbers = [
                int("".join(c for c in user["TP_number"] if c.isdigit()))
                for user in users
                if user["TP_number"].startswith(role_prefix.get(role, ""))
                and any(char.isdigit() for char in user["TP_number"])
            ]

            last_tp_number = max(numeric_tp_numbers) if numeric_tp_numbers else 0
            new_tp_number = f"{role_prefix.get(role)}{last_tp_number + 1}"
            print(f"\nAssigned TP Number: {new_tp_number}")

            # Collect user details
            name = input("Enter Name (or 'QUIT' to cancel): ").strip()
            if name.lower() == "quit":
                continue

            # Ensure password meets minimum length requirement
            while True:
                password = input("Enter Password (or 'QUIT' to cancel): ").strip()
                if password.lower() == "quit":
                    continue
                if len(password) < 6:
                    print("Password must be at least 6 characters long. Try again.")
                else:
                    break

            # Create new user record
            new_user = {
                "TP_number": new_tp_number,
                "Role": role,
                "Name": name,
                "Password": password,
            }
            add_row("../DATA/user", new_user)
            print_separator("User Added Successfully")

            # If user is a student, collect additional details
            if role == "Student":
                print_separator("Enter Student Details")
                student_detail = {
                    "TP_number": new_tp_number,
                    "Name": name,
                    "Password": password,
                    "Date_of_birth": input(
                        "Enter Date of Birth (YYYY-MM-DD): "
                    ).strip(),
                    "Contact": input("Enter Contact Number: ").strip(),
                    "Address": input("Enter Address: ").strip(),
                    "Emergency_contact": input("Enter Emergency Contact: ").strip(),
                    "Emergency_relationship": input(
                        "Enter Emergency Contact Relationship: "
                    ).strip(),
                }

                # Validate course ID and retrieve course details
                while True:
                    course_id = input("Enter Course ID: ").strip().upper()
                    course_match = next(
                        (c for c in course_data if c["Course_id"] == course_id), None
                    )
                    if course_match:
                        student_detail["Course_id"] = course_id
                        student_detail["Course"] = course_match["Course"]
                        tuition_fee = float(
                            course_match["School_fee"]
                        )  # Get tuition fee from course.txt
                        break
                    else:
                        print("Invalid Course ID. Please try again.")

                add_row("../DATA/studentdetail", student_detail)
                print_separator("Student Details Added Successfully")

                # Enroll student in a group
                print_separator("Enrollment")
                while True:
                    group = input("Enter Group (A or B): ").strip().upper()
                    if group in ["A", "B"]:
                        break
                    print("Invalid input. Please enter 'A' or 'B'.")

                enrollment_detail = {
                    "TP_number": new_tp_number,
                    "Course_id": student_detail["Course_id"],
                    "Course": student_detail["Course"],
                    "Group": group,
                }
                add_row("../DATA/enrolment", enrollment_detail)
                print_separator("Enrollment Added Successfully")

                # Handle student financial records
                print_separator("Financial Record")
                while True:
                    try:
                        amount_paid = float(input("Enter Amount Paid: ").strip())
                        if amount_paid > tuition_fee:
                            print(
                                "Amount paid cannot be greater than the tuition fee. Try again."
                            )
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                balance = tuition_fee - amount_paid
                payment_status = "Completed" if balance == 0 else "Pending"
                financial_detail = {
                    "TP_number": new_tp_number,
                    "Tuition_fee": tuition_fee,
                    "Amount_paid": amount_paid,
                    "Balance": balance,
                    "Payment_status": payment_status,
                }
                add_row("../DATA/financial", financial_detail)
                print_separator("Financial Record Added Successfully")

        elif choice == "Update user details":
            print_separator("Updating User Details")
            update_entity("TP_number", "TP_number", "../DATA/studentdetail")

        elif choice == "Delete a user":
            print_separator("Delete a User")
            while True:
                tp_number = input(
                    "Enter TP Number of the user to delete (or 'QUIT' to cancel): "
                ).strip()
                if tp_number.upper() == "QUIT":
                    break
                row = get_row("../DATA/user", "TP_number", tp_number)
                if not row:
                    print("User not found! Please try again.")
                    continue
                print_separator("User Found")
                print(f"User Details: {row}")
                confirm = prompt(
                    "Are you sure you want to delete this user?", ["Yes", "No", "QUIT"]
                )
                if confirm in ["No", "QUIT"]:
                    print("Deletion canceled.")
                    break
                delete_row("../DATA/user", "TP_number", tp_number)
                delete_row("../DATA/enrolment", "TP_number", tp_number)
                delete_row("../DATA/financial", "TP_number", tp_number)
                delete_row("../DATA/studentdetail", "TP_number", tp_number)
                print_separator(
                    f"User {tp_number} and related records deleted successfully!"
                )
                break
