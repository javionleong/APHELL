# Import common modules
from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def course_management():
    course_data_path = "../DATA/course"
    course_subject_path = "../DATA/course_subject"

    while True:
        print_separator("COURSE MANAGEMENT MENU")

        # Prompt admin for an action
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all Course",
                "Add a Course",
                "Update Course",
                "Update Course_Subject",
                "Delete a Course",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print_separator("\nBye bye, Admin\n")
            break

        elif choice == "View all Course":
            print_separator("List of Courses")
            table(f"{course_data_path}.txt")

        elif choice == "Add a Course":
            print_separator("Add a New Course")
            courses = get_all_rows(course_data_path)

            # Generate Course_id automatically
            if courses:
                existing_course_ids = [
                    int(course["Course_id"][1:])
                    for course in courses
                    if course["Course_id"][1:].isdigit()
                ]
                new_course_id = (
                    f"C{max(existing_course_ids) + 1}" if existing_course_ids else "C1"
                )
            else:
                new_course_id = "C1"

            print(f"Generated Course ID: {new_course_id}")

            # Get course details
            new_course_name = input("Enter Course Name (or 'QUIT' to cancel): ").strip()
            if new_course_name.upper() == "QUIT":
                continue
            if not new_course_name:
                print("Error: Course Name cannot be empty.")
                continue

            # Get school fee
            while True:
                new_school_fee = input(
                    "Enter School Fee (or 'QUIT' to cancel): "
                ).strip()
                if new_school_fee.upper() == "QUIT":
                    break
                try:
                    new_school_fee = float(new_school_fee)
                    if new_school_fee <= 0:
                        print("Error: School Fee must be a positive number.")
                    else:
                        break
                except ValueError:
                    print("Error: Please enter a valid number for the School Fee.")

            if new_school_fee == "QUIT":
                continue

            # Get subjects
            subject1 = input("Enter Subject 1 (or 'QUIT' to cancel): ").strip()
            if subject1.upper() == "QUIT":
                continue

            subject2 = input("Enter Subject 2 (or 'QUIT' to cancel): ").strip()
            if subject2.upper() == "QUIT":
                continue

            if not subject1 or not subject2:
                print("Error: Both subjects must be provided.")
                continue

            # Save course details
            new_course = {
                "Course_id": new_course_id,
                "Course": new_course_name,
                "School_fee": str(new_school_fee),
            }
            add_row(course_data_path, new_course)

            # Save course subjects
            new_course_subject = {
                "Course_id": new_course_id,
                "Course": new_course_name,
                "Subject1": subject1,
                "Subject2": subject2,
            }
            add_row(course_subject_path, new_course_subject)

            print_separator(
                f"Course {new_course_id} added successfully with subjects {subject1} and {subject2}!"
            )

        elif choice == "Update Course":
            print_separator("Update Course")
            update_entity("course", "Course_id", course_data_path)

        elif choice == "Update Course_Subject":
            print_separator("Update Course Subjects")
            update_entity("Course_Subject", "Course_id", course_subject_path)

        elif choice == "Delete a Course":
            print_separator("Delete a Course")
            courses = get_all_rows(course_data_path)
            if not courses:
                print("No courses available to delete.")
                continue

            # List available courses for deletion
            course_options = {
                course["Course_id"]: course["Course"] for course in courses
            }
            course_options["QUIT"] = "Cancel"

            selected_course_id = prompt(
                "Select a course to delete (or 'QUIT' to cancel):",
                list(course_options.keys()),
            )

            if selected_course_id == "QUIT":
                continue

            # Confirm and delete course
            row = get_row(course_data_path, "Course_id", selected_course_id)
            if not row:
                print("Course not found! Please try again.")
                continue

            print(f"Course found: {row}")

            confirm = prompt(
                "Are you sure you want to delete this course?", ["Yes", "No", "QUIT"]
            )

            if confirm in ["QUIT", "No"]:
                print("Deletion canceled.")
                continue
            delete_row(course_subject_path, "Course_id", selected_course_id)
            delete_row(course_data_path, "Course_id", selected_course_id)
            print_separator(f"Course {selected_course_id} deleted successfully!")
