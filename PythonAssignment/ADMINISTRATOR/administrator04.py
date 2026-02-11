from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def class_schedule():
    """Manage class schedules (View, Add, Delete)."""

    while True:
        print_separator("CLASS SCHEDULE MANAGEMENT MENU")

        # Prompt admin for an action choice
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View class schedules",
                "Add a class schedule",
                "Delete a class schedule",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print_separator("\nBye bye, Admin\n")
            break

        elif choice == "View class schedules":
            # Display all class schedules
            print_separator("VIEW CLASS SCHEDULES")
            table("../DATA/class_schedule.txt")

        elif choice == "Add a class schedule":
            print_separator("ADD CLASS SCHEDULE")

            # Retrieve course and subject details
            course_subjects = get_all_rows("../DATA/course_subject")

            # Prompt for Course ID
            course_id = prompt(
                "Select a Course ID:", [row["Course_id"] for row in course_subjects]
            )

            # Find selected course details
            selected_course = next(
                row for row in course_subjects if row["Course_id"] == course_id
            )

            # Prompt for subject selection
            subject = prompt(
                "Select a Subject:",
                [selected_course["Subject1"], selected_course["Subject2"]],
            )

            # Retrieve teacher TP numbers
            teacher_tp_numbers = [
                row["TP_number"]
                for row in get_all_rows("../DATA/user")
                if row["Role"] == "Teacher"
            ]

            # Prompt for teacher selection
            tp_number = prompt("Select TP Number (Teacher Only):", teacher_tp_numbers)

            # Get class date and time
            date = input("Enter Class Date (DD-MM-YYYY): ")
            time = input("Enter Class Time (e.g., 9:00 AM - 11:00 AM): ")

            # Prompt for room and group selection
            room = prompt("Select the Room:", ["Room A", "Room B"])
            group = prompt("Select Group:", ["A", "B"])

            # Retrieve existing class schedules
            existing_schedules = get_all_rows("../DATA/class_schedule") or []

            # Generate a new unique Class ID
            if existing_schedules:
                last_class_id = max(
                    int("".join(filter(str.isdigit, schedule["Class_id"])))
                    for schedule in existing_schedules
                )
                new_class_id = f"Class{last_class_id + 1}"
            else:
                new_class_id = "Class1"  # Start from Class1 if no records exist

            # Check for time and room conflicts
            if any(
                schedule["Date"] == date
                and schedule["Time"] == time
                and schedule["Room"].lower() == room.lower()
                for schedule in existing_schedules
            ):
                print("Error: The time and room are already booked for this date!")
                continue

            # Create new schedule entry
            new_schedule = {
                "Class_id": new_class_id,  # Auto-generated Class_id
                "Course_id": course_id,
                "Subject": subject,
                "TP_number": tp_number,
                "Date": date,
                "Time": time,
                "Room": room,
                "Group": group,
                "Status": "Active",
            }

            # Add new schedule to the data file
            add_row("../DATA/class_schedule", new_schedule)

            # Display the newly added schedule
            print_separator("CLASS SCHEDULE DETAILS")
            print(", ".join(f"{key}: {value}" for key, value in new_schedule.items()))
            print("\nClass schedule added successfully!\n")

        elif choice == "Delete a class schedule":
            print_separator("DELETE CLASS SCHEDULE")

            # Retrieve all class schedules
            schedules = get_all_rows("../DATA/class_schedule")

            if not schedules:
                print("No class schedules available to delete.")
                continue

            # Prompt for Class ID to delete
            class_id = prompt(
                "Enter the Class ID to delete:",
                list(set([row["Class_id"] for row in schedules])),
            )

            # Find the selected class schedule
            row = next((r for r in schedules if r["Class_id"] == class_id), None)

            if not row:
                print(f"No class schedule found for Class ID '{class_id}'.")
                continue

            # Display the class schedule before deletion
            print("\nClass schedule found:")
            print(", ".join(f"{key}: {value}" for key, value in row.items()))

            # Confirm deletion - Fixed the type error by breaking into two steps
            confirmation = prompt(
                "Are you sure you want to delete this schedule?", ["Yes", "No"]
            )
            if confirmation == "Yes":
                # Remove schedule from file
                write(
                    [r for r in schedules if r["Class_id"] != class_id],
                    "../DATA/class_schedule.txt",
                )
                print(f"Class schedule with Class ID '{class_id}' has been deleted.")
            else:
                print("Deletion cancelled.")
