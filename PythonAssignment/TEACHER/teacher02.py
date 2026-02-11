from COMMON.design import print_separator
from COMMON.prompt import *
from COMMON.csv import *


def student_enrolment(user):
    data_path = "../DATA/enrolment.txt"

    while True:
        print_separator("Enrolment Menu")
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all student enrolments",
                "Remove a student from a course",
                "Update student enrolment details",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print("Exiting Enrolment Management....")
            break

        elif choice == "View all student enrolments":
            print_separator("Student Enrolment")
            table(data_path)
            input("\nPress Enter to continue...")

        elif choice == "Remove a student from a course":
            print_separator("Current Enrolments")
            table(data_path)

            # Fetch all enrolments
            enrolments = get_all_rows("../DATA/enrolment")

            # Get unique TP numbers from enrolments
            tp_numbers = list(set(row["TP_number"] for row in enrolments))

            if not tp_numbers:
                print("No students are currently enrolled in any courses.")
                continue

            tp_numbers.append("Back")
            tp_number = prompt("Select a student to remove:", tp_numbers)

            if tp_number == "Back":
                continue

            # Get courses this student is enrolled in
            student_courses = [
                f"{row['Course_id']} - {row['Course']}"
                for row in enrolments
                if row["TP_number"] == tp_number
            ]

            if not student_courses:
                print(f"Student {tp_number} is not enrolled in any courses.")
                continue

            student_courses.append("Back")
            selected = prompt(
                f"Select a course to remove {tp_number} from:", student_courses
            )

            if selected == "Back":
                continue

            # Extract Course_id from selection
            course_id = selected.split(" - ")[0]

            # Confirm removal
            confirm = prompt(
                f"Are you sure you want to remove {tp_number} from {selected}?",
                ["Yes", "No"],
            )

            if confirm == "Yes":
                # Filter out the specific enrolment
                updated_enrolments = [
                    row
                    for row in enrolments
                    if not (
                        row["TP_number"] == tp_number and row["Course_id"] == course_id
                    )
                ]

                write(updated_enrolments, data_path)
                print(f"Student {tp_number} removed from {selected}.")
            else:
                print("Removal cancelled.")

        elif choice == "Update student enrolment details":
            print_separator("Update Enrolment")
            table(data_path)

            # Get all enrolments
            enrolments = get_all_rows("../DATA/enrolment")

            # Get unique TP numbers
            tp_numbers = list(set(row["TP_number"] for row in enrolments))
            tp_numbers.append("Back")

            # Select student
            tp_number = prompt("Select student to update:", tp_numbers)
            if tp_number == "Back":
                continue

            # Get student's current enrolment
            current_enrolment = next(
                (row for row in enrolments if row["TP_number"] == tp_number), None
            )

            if not current_enrolment:
                print(f"No enrolment found for {tp_number}")
                continue

            print(f"\nCurrent enrolment for {tp_number}:")
            print(f"Course ID: {current_enrolment['Course_id']}")
            print(f"Course: {current_enrolment['Course']}")
            print(f"Group: {current_enrolment['Group']}")

            # Update group
            new_group = input(
                f"\nEnter new Group (current: {current_enrolment['Group']}, press Enter to keep current): "
            ).strip()
            if new_group:
                # Update the enrolment
                for row in enrolments:
                    if row["TP_number"] == tp_number:
                        row["Group"] = new_group

                write(enrolments, data_path)
                print(f"\nGroup updated successfully for {tp_number}")
            else:
                print("\nNo changes made")
