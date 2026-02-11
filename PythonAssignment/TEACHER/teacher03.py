from COMMON.design import print_separator
from COMMON.query import *
from COMMON.prompt import *
from COMMON.csv import *


def grade_management(user):
    data_path = "../DATA/grades.txt"

    while True:
        print_separator("Grade Management")
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all grades",
                "Add a grade",
                "Remove a grade",
                "Update grade details",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print("Exiting Grade Management....")
            break

        elif choice == "View all grades":
            print_separator("Grades")
            table(data_path)
            input("\nPress Enter to continue...")

        elif choice == "Add a grade":
            print_separator("Add Grade")
            table(data_path)

            print("\nNote: Type 'Back' at any prompt to return to the main menu")

            tp_number = input(
                "Enter student TP_number (or 'Back' to go back): "
            ).strip()
            if tp_number.lower() == "back":
                continue

            course_id = input("Enter Course_id (or 'Back' to go back): ").strip()
            if course_id.lower() == "back":
                continue

            # Get subjects
            try:
                courses = get_all_rows("../DATA/course_subject")
                subjects = []

                for course in courses:
                    if course["Course_id"] == course_id:
                        subjects = [
                            value
                            for key, value in course.items()
                            if key.startswith("Subject") and value
                        ]
                        break

                if not subjects:
                    print(f"No subjects found for Course_id: {course_id}")
                    continue

                subjects.append("Back")
                subject = prompt("Select a Subject:", subjects)
                if subject == "Back":
                    continue

            except Exception as e:
                print(f"Error loading subjects: {e}")
                continue

            assessment_type = prompt(
                "Select Assessment_type:", ["Assignment", "Exam", "Back"]
            )
            if assessment_type == "Back":
                continue

            grades = get_all_rows("../DATA/grades")

            # Check for existing grade
            if any(
                row["TP_number"] == tp_number
                and row["Subject"] == subject
                and row["Assessment_type"] == assessment_type
                for row in grades
            ):
                print(
                    f"Student {tp_number} already has a {assessment_type} grade for {subject}."
                )

                update_choice = prompt(
                    "Would you like to update the existing grade?", ["Yes", "No"]
                )
                if update_choice == "No":
                    continue

                updated_grades = [
                    row
                    for row in grades
                    if not (
                        row["TP_number"] == tp_number
                        and row["Subject"] == subject
                        and row["Assessment_type"] == assessment_type
                    )
                ]
                write(updated_grades, data_path)
                print(f"Previous {assessment_type} grade for {subject} removed.")

            while True:
                grade = input("Enter Grade (0-100) (or 'Back' to go back): ").strip()
                if grade.lower() == "back":
                    continue
                if grade.isdigit() and 0 <= int(grade) <= 100:
                    break
                print("Invalid input. Please enter a number between 0 and 100.")

            feedback = input("Enter Feedback (or 'Back' to go back): ").strip()
            if feedback.lower() == "back":
                continue

            new_grade = {
                "TP_number": tp_number,
                "Course_id": course_id,
                "Assessment_type": assessment_type,
                "Subject": subject,
                "Grade": grade,
                "Feedback": feedback,
            }

            add_row("../DATA/grades", new_grade)
            print(
                f"{assessment_type} grade for {tp_number} in {subject} successfully recorded."
            )

        elif choice == "Remove a grade":
            print_separator("Remove Grade")
            table(data_path)

            print("\nNote: Type 'Back' at any prompt to return to the main menu")

            grades = get_all_rows("../DATA/grades")
            tp_numbers = list(set(row["TP_number"] for row in grades))

            if not tp_numbers:
                print("No grades found in the system.")
                continue

            tp_numbers.append("Back")
            tp_number = prompt("Select student TP_number:", tp_numbers)
            if tp_number == "Back":
                continue

            student_grades = [row for row in grades if row["TP_number"] == tp_number]

            if not student_grades:
                print(f"No grades found for TP_number {tp_number}.")
                continue

            print("\nGrades for Student:", tp_number)
            selected_table(student_grades)

            grade_options = [
                f"{row['Subject']} - {row['Assessment_type']}" for row in student_grades
            ]
            grade_options.append("Back")

            selected = prompt("Select a grade to remove:", grade_options)
            if selected == "Back":
                continue

            subject, assessment_type = selected.split(" - ")

            confirm = prompt(
                f"Are you sure you want to remove the {assessment_type} grade for {subject}?",
                ["Yes", "No"],
            )
            if confirm == "No":
                print("Grade removal cancelled.")
                continue

            updated_grades = [
                row
                for row in grades
                if not (
                    row["TP_number"] == tp_number
                    and row["Subject"] == subject
                    and row["Assessment_type"] == assessment_type
                )
            ]

            if len(updated_grades) == len(grades):
                print("Grade not found.")
            else:
                write(updated_grades, data_path)
                print(
                    f"{assessment_type} grade for {tp_number} in {subject} removed successfully."
                )

        elif choice == "Update grade details":
            print_separator("Update Grade")
            table(data_path)

            grades = get_all_rows("../DATA/grades")
            tp_numbers = list(set(row["TP_number"] for row in grades))

            if not tp_numbers:
                print("No grades found in the system.")
                continue

            tp_numbers.append("Back")
            tp_number = prompt("Select student TP_number to update:", tp_numbers)

            if tp_number == "Back":
                continue

            student_grades = [row for row in grades if row["TP_number"] == tp_number]
            print("\nCurrent grades for", tp_number)
            selected_table(student_grades)

            grade_options = [
                f"{row['Subject']} - {row['Assessment_type']}" for row in student_grades
            ]
            grade_options.append("Back")

            selected = prompt("Select grade to update:", grade_options)
            if selected == "Back":
                continue

            subject, assessment_type = selected.split(" - ")

            current_grade = next(
                (
                    row
                    for row in grades
                    if row["TP_number"] == tp_number
                    and row["Subject"] == subject
                    and row["Assessment_type"] == assessment_type
                ),
                None,
            )

            if current_grade:
                print(f"\nCurrent Grade: {current_grade['Grade']}")
                print(f"Current Feedback: {current_grade['Feedback']}")

                while True:
                    new_grade = input(
                        "\nEnter new Grade (0-100, or press Enter to keep current): "
                    ).strip()
                    if not new_grade:
                        new_grade = current_grade["Grade"]
                        break
                    if new_grade.isdigit() and 0 <= int(new_grade) <= 100:
                        break
                    print("Invalid input. Please enter a number between 0 and 100.")

                new_feedback = input(
                    "Enter new Feedback (or press Enter to keep current): "
                ).strip()
                if not new_feedback:
                    new_feedback = current_grade["Feedback"]

                # Update the grade
                for row in grades:
                    if (
                        row["TP_number"] == tp_number
                        and row["Subject"] == subject
                        and row["Assessment_type"] == assessment_type
                    ):
                        row["Grade"] = new_grade
                        row["Feedback"] = new_feedback

                write(grades, data_path)
                print("\nGrade updated successfully!")
            else:
                print("Grade not found.")
