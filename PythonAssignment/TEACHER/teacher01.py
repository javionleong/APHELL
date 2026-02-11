import os
import sys

# Add parent directory to Python path so COMMON can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from COMMON.prompt import *
from COMMON.csv import *
from COMMON.design import print_separator
from COMMON.query import *


def view_schedules(teacher_tp):
    print_separator("My Course Schedule")

    # Get schedules using query.py's get_all_rows
    schedules = get_all_rows("../DATA/class_schedule")
    teacher_schedules = [s for s in schedules if s["TP_number"] == teacher_tp]

    if not teacher_schedules:
        print(f"No schedules found for your account.")
        input("\nPress Enter to continue...")
        return

    # Display teacher's schedules first
    print(f"Your current schedules:")
    print_separator()

    # Sort schedules before displaying
    teacher_schedules.sort(key=lambda x: (x["Date"], x["Time"]))
    selected_table(teacher_schedules)

    # Get unique course IDs for prompt
    course_ids = list(set(s["Course_id"] for s in teacher_schedules))
    course_ids.append("Back")

    # Use prompt.py's prompt function for selection
    course_id = prompt("\nSelect Course_id to view detailed schedule:", course_ids)
    if course_id == "Back":
        return

    # Filter and display detailed view for selected course
    course_schedules = [s for s in teacher_schedules if s["Course_id"] == course_id]

    print(f"\nDetailed Schedule for Course: {course_id}")
    print_separator()

    # Use selected_table for detailed view
    selected_table(course_schedules)

    input("\nPress Enter to continue...")


def course_management(user):
    teacher = user
    # First, require teacher login
    if not teacher:
        return

    data_path = "../DATA/subject_data.txt"
    schedule_path = "../DATA/class_schedule.txt"

    # Check if files exist, if not create them
    for path in [data_path, schedule_path]:
        if not os.path.exists(path):
            print(f"Creating file: {path}")
            with open(path, "w") as f:
                if "subject_data" in path:
                    f.write("Course_id,Subject,Material_type,Link\n")
                else:
                    f.write("Course_id,Subject,TP_number,Date,Time,Room,Group,Status\n")

    while True:
        print_separator(f"Course Management - Teacher {teacher['TP_number']}")
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all courses",
                "View my schedule",  # Changed option name
                "Add course material",
                "Edit course material",
                "Remove course material",
                "Edit course schedule",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print("Exiting Course Management....")
            break

        elif choice == "View all courses":
            print_separator("Course Materials")
            table(data_path)
            input("\nPress Enter to continue...")

        elif choice == "View my schedule":  # Modified this section
            view_schedules(teacher["TP_number"])

        elif choice == "Add course material":
            print_separator("Add Course Material")
            table(data_path)

            print("\nNote: Type 'Back' at any prompt to return to the main menu")

            # Get course selection
            course_data = get_all_rows("../DATA/subject_data")
            course_ids = list(set(row["Course_id"] for row in course_data))
            course_ids.append("Back")

            course_id = prompt("Select Course_id:", course_ids)
            if course_id == "Back":
                continue

            # Get subject selection
            subjects = list(
                set(
                    row["Subject"]
                    for row in course_data
                    if row["Course_id"] == course_id
                )
            )
            if not subjects:
                print(f"No subjects found for Course {course_id}")
                continue

            subjects.append("Back")
            subject = prompt("Select Subject:", subjects)
            if subject == "Back":
                continue

            # Get material type
            material_type = prompt(
                "Select Material_type:",
                [
                    "Lecturer Note",
                    "Assignment",
                    "Announcement",
                    "Quiz",
                    "Exam",
                    "Other",
                    "Back",
                ],
            )
            if material_type == "Back":
                continue

            if material_type == "Other":
                material_type = input("Enter custom Material_type: ")

            link = input("Enter Link (or 'Back' to go back): ").strip()
            if link.lower() == "back":
                continue

            new_material = {
                "Course_id": course_id,
                "Subject": subject,
                "Material_type": material_type,
                "Link": link,
            }

            add_row("../DATA/subject_data", new_material)
            print("Course material added successfully!")

        elif choice == "Edit course material":
            print_separator("Edit Course Material")
            table(data_path)

            materials = get_all_rows("../DATA/subject_data")
            if not materials:
                print("No course materials found in the system.")
                continue

            course_ids = list(set(row["Course_id"] for row in materials))
            course_ids.append("Back")

            course_id = prompt("Select Course_id:", course_ids)
            if course_id == "Back":
                continue

            course_materials = [m for m in materials if m["Course_id"] == course_id]
            if not course_materials:
                print(f"No materials found for Course {course_id}")
                continue

            print("\nCurrent materials:")
            selected_table(course_materials)

            material_options = [
                f"{m['Subject']} - {m['Material_type']}" for m in course_materials
            ]
            material_options.append("Back")

            selected = prompt("Select material to edit:", material_options)
            if selected == "Back":
                continue

            subject, material_type = selected.split(" - ")

            current_material = next(
                (
                    m
                    for m in materials
                    if m["Course_id"] == course_id
                    and m["Subject"] == subject
                    and m["Material_type"] == material_type
                ),
                None,
            )

            if current_material:
                print(f"\nCurrent Link: {current_material['Link']}")
                new_link = input(
                    "Enter new Link (or press Enter to keep current): "
                ).strip()

                if new_link:
                    for row in materials:
                        if (
                            row["Course_id"] == course_id
                            and row["Subject"] == subject
                            and row["Material_type"] == material_type
                        ):
                            row["Link"] = new_link

                    write(materials, data_path)
                    print("\nMaterial updated successfully!")
                else:
                    print("\nNo changes made.")
            else:
                print("Material not found.")

        elif choice == "Remove course material":
            print_separator("Remove Course Material")
            table(data_path)

            materials = get_all_rows("../DATA/subject_data")
            if not materials:
                print("No course materials found in the system.")
                continue

            course_ids = list(set(row["Course_id"] for row in materials))
            course_ids.append("Back")

            course_id = prompt("Select Course_id:", course_ids)
            if course_id == "Back":
                continue

            course_materials = [m for m in materials if m["Course_id"] == course_id]
            if not course_materials:
                print(f"No materials found for Course {course_id}")
                continue

            print("\nCurrent materials:")
            selected_table(course_materials)

            material_options = [
                f"{m['Subject']} - {m['Material_type']}" for m in course_materials
            ]
            material_options.append("Back")

            selected = prompt("Select material to remove:", material_options)
            if selected == "Back":
                continue

            subject, material_type = selected.split(" - ")

            confirm = prompt(
                f"Are you sure you want to remove {material_type} for {subject}?",
                ["Yes", "No"],
            )
            if confirm == "No":
                print("Removal cancelled.")
                continue

            updated_materials = [
                m
                for m in materials
                if not (
                    m["Course_id"] == course_id
                    and m["Subject"] == subject
                    and m["Material_type"] == material_type
                )
            ]

            write(updated_materials, data_path)
            print(f"Material removed successfully!")

        elif choice == "Edit course schedule":
            print_separator("Edit Course Schedule")
            table(schedule_path)

            schedules = get_all_rows("../DATA/class_schedule")
            if not schedules:
                print("No schedules found in the system.")
                continue

            course_ids = list(set(row["Course_id"] for row in schedules))
            course_ids.append("Back")

            course_id = prompt("Select Course_id:", course_ids)
            if course_id == "Back":
                continue

            course_schedules = [s for s in schedules if s["Course_id"] == course_id]
            if not course_schedules:
                print(f"No schedules found for Course {course_id}")
                continue

            schedule_options = [
                f"{s['Subject']} - {s['Date']} ({s['Time']})" for s in course_schedules
            ]
            schedule_options.append("Back")

            selected = prompt("Select schedule to edit:", schedule_options)
            if selected == "Back":
                continue

            subject = selected.split(" - ")[0]
            date_time = " - ".join(selected.split(" - ")[1:])
            date = date_time.split(" (")[0]
            time = date_time.split("(")[1].rstrip(")")

            current_schedule = next(
                (
                    s
                    for s in schedules
                    if s["Course_id"] == course_id
                    and s["Subject"] == subject
                    and s["Date"] == date
                    and s["Time"] == time
                ),
                None,
            )

            if current_schedule:
                print("\nCurrent schedule details:")
                for key, value in current_schedule.items():
                    if key not in ["Course_id", "Subject"]:
                        print(f"{key}: {value}")

                print("\nEnter new values (or press Enter to keep current):")
                new_date = (
                    input(f"Date (YYYY-MM-DD): ").strip() or current_schedule["Date"]
                )
                new_time = (
                    input(f"Time (HH:MM AM/PM - HH:MM AM/PM): ").strip()
                    or current_schedule["Time"]
                )
                new_room = input(f"Room: ").strip() or current_schedule["Room"]
                new_group = input(f"Group: ").strip() or current_schedule["Group"]
                new_status = prompt(
                    "Select Status:",
                    ["Active", "Completed", "Cancelled", "Keep Current"],
                )

                if new_status == "Keep Current":
                    new_status = current_schedule["Status"]

                # Show summary of changes
                print("\nProposed changes:")
                print(f"Date: {current_schedule['Date']} -> {new_date}")
                print(f"Time: {current_schedule['Time']} -> {new_time}")
                print(f"Room: {current_schedule['Room']} -> {new_room}")
                print(f"Group: {current_schedule['Group']} -> {new_group}")
                print(f"Status: {current_schedule['Status']} -> {new_status}")

                confirm = prompt("\nSave these changes?", ["Yes", "No"])
                if confirm == "Yes":
                    for schedule in schedules:
                        if (
                            schedule["Course_id"] == course_id
                            and schedule["Subject"] == subject
                            and schedule["Date"] == date
                            and schedule["Time"] == time
                        ):
                            schedule["Date"] = new_date
                            schedule["Time"] = new_time
                            schedule["Room"] = new_room
                            schedule["Group"] = new_group
                            schedule["Status"] = new_status

                    write(schedules, schedule_path)
                    print("\nSchedule updated successfully!")
                else:
                    print("\nNo changes made.")
            else:
                print("Schedule not found.")
