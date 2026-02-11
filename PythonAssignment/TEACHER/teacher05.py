from COMMON.design import print_separator
from COMMON.prompt import *
from COMMON.csv import *

DATA_PATH = "../DATA/"


def report_generation(user):
    while True:
        print_separator("Report Generation")
        choice = prompt(
            "Select a report to generate (enter 'Exit' to quit):",
            [
                "Student Performance Report",
                "Attendance Report",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print("Exiting Report Generation...")
            break

        elif choice == "Student Performance Report":
            print_separator("Student Performance Report")

            # Get all grades
            grades = get_all_rows(DATA_PATH + "grades")
            if not grades:
                print("No grade records found in the system.")
                continue

            # Get unique TP numbers from grades
            tp_numbers = list(set(row["TP_number"] for row in grades))
            tp_numbers.append("Back")

            # Prompt for TP number selection
            tp_number = prompt("Select student TP_number:", tp_numbers)
            if tp_number == "Back":
                continue

            # Filter grades for selected student
            student_grades = [row for row in grades if row["TP_number"] == tp_number]

            if not student_grades:
                print(f"No grade records found for {tp_number}.")
                continue

            # Display student performance report
            print(f"\nPerformance Report for Student: {tp_number}")
            print("-" * 60)
            print("Subject | Assessment_type | Grade | Feedback")
            print("-" * 60)

            # Group grades by subject
            for grade in student_grades:
                print(
                    f"{grade['Subject']:<8} | "
                    f"{grade['Assessment_type']:<15} | "
                    f"{grade['Grade']:<5} | "
                    f"{grade['Feedback']}"
                )

            print("-" * 60)

            # Calculate and show average grade
            total_grade = sum(float(grade["Grade"]) for grade in student_grades)
            average_grade = total_grade / len(student_grades)
            print(f"\nAverage Grade: {average_grade:.2f}")

            # Wait for user input before continuing
            input("\nPress Enter to continue...")

        elif choice == "Attendance Report":
            print_separator("Attendance Report")
            table(DATA_PATH + "attendance.txt")

            input("\nPress Enter to continue...")
