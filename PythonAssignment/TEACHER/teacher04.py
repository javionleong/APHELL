from COMMON.csv import *
from COMMON.prompt import *
from COMMON.query import *
from COMMON.design import *


def attendance_management(user):
    while True:
        print_separator("Attendance Management")
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all attendance records",
                "Record student attendance",
                "Remove an attendance record",
                "Update attendance details",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print("Exiting Attendance Management....")
            break

        elif choice == "View all attendance records":
            print_separator()
            table("../DATA/attendance.txt")
            input("\nPress Enter to continue...")

        elif choice == "Record student attendance":
            print_separator("Record Student Attendance")

            course_subject_data = get_all_rows("../DATA/subject_data")
            course_ids = {row["Course_id"] for row in course_subject_data}

            if not course_ids:
                print("No course subject data found.")
                continue

            course_list = list(course_ids)
            course_list.append("Back")
            selected_course_id = prompt("Select a Course_id:", course_list)

            if selected_course_id == "Back":
                continue

            selected_subjects = [
                row
                for row in course_subject_data
                if row["Course_id"] == selected_course_id
            ]
            if not selected_subjects:
                print(f"No subjects found under Course {selected_course_id}.")
                continue

            subject_list = list(set(row["Subject"] for row in selected_subjects))
            subject_list.append("Back")
            selected_subject = prompt("Select a Subject:", subject_list)

            if selected_subject == "Back":
                continue

            enrolment_data = get_all_rows("../DATA/enrolment")
            enrolled_students = [
                row for row in enrolment_data if row["Course_id"] == selected_course_id
            ]

            if not enrolled_students:
                print(
                    f"No currently enrolled students found in {selected_subject} under Course {selected_course_id}."
                )
                continue

            print_separator()
            print("\nCurrently Enrolled Students:")
            for student in enrolled_students:
                print(f"- {student['TP_number']} ({student['Course_id']})")

            print("\nNote: Type 'Back' at any prompt to return to the main menu")

            date = input("\nEnter Date (YYYY-MM-DD) or 'Back': ").strip()
            if date.lower() == "back":
                continue

            attendance_records = get_all_rows("../DATA/attendance")

            while True:
                tp_number = (
                    input(
                        "\nEnter TP_number (or 'done' to finish, 'Back' for main menu): "
                    )
                    .strip()
                    .upper()
                )
                if tp_number.lower() == "back":
                    break
                if tp_number.lower() == "done":
                    break

                if not any(s["TP_number"] == tp_number for s in enrolled_students):
                    print(
                        f"{tp_number} is not currently enrolled in {selected_subject}. Try again."
                    )
                    continue

                status = prompt("Select Status", ["Present", "Absent", "Late", "Back"])
                if status == "Back":
                    continue

                if any(
                    row["TP_number"] == tp_number
                    and row["Date"] == date
                    and row["Subject"] == selected_subject
                    for row in attendance_records
                ):
                    print(
                        f"Attendance for {tp_number} in {selected_subject} on {date} is already recorded."
                    )
                    continue

                attendance_data = {
                    "TP_number": tp_number,
                    "Course_id": selected_course_id,
                    "Subject": selected_subject,
                    "Date": date,
                    "Status": status,
                }
                add_row("../DATA/attendance", attendance_data)
                print(
                    f"Attendance recorded for {tp_number} in {selected_subject} on {date}."
                )

        elif choice == "Remove an attendance record":
            print_separator("Remove Attendance Record")
            table("../DATA/attendance.txt")

            attendance_records = get_all_rows("../DATA/attendance")
            if not attendance_records:
                print("No attendance records found.")
                continue

            tp_numbers = list(set(row["TP_number"] for row in attendance_records))
            tp_numbers.append("Back")

            tp_number = prompt("Select TP_number to remove:", tp_numbers)
            if tp_number == "Back":
                continue

            student_courses = list(
                set(
                    row["Course_id"]
                    for row in attendance_records
                    if row["TP_number"] == tp_number
                )
            )
            student_courses.append("Back")

            course_id = prompt(f"Select Course_id for {tp_number}:", student_courses)
            if course_id == "Back":
                continue

            student_dates = list(
                set(
                    row["Date"]
                    for row in attendance_records
                    if row["TP_number"] == tp_number and row["Course_id"] == course_id
                )
            )
            student_dates.append("Back")

            date = prompt(f"Select Date for {tp_number} in {course_id}:", student_dates)
            if date == "Back":
                continue

            student_subjects = list(
                set(
                    row["Subject"]
                    for row in attendance_records
                    if row["TP_number"] == tp_number
                    and row["Course_id"] == course_id
                    and row["Date"] == date
                )
            )
            student_subjects.append("Back")

            subject = prompt(
                f"Select Subject for {tp_number} on {date}:", student_subjects
            )
            if subject == "Back":
                continue

            matching_records = [
                row
                for row in attendance_records
                if row["TP_number"] == tp_number
                and row["Date"] == date
                and row["Subject"] == subject
                and row["Course_id"] == course_id
            ]

            if not matching_records:
                print("Attendance record not found.")
                continue

            print("\nRecord to be deleted:")
            print(f"Student: {tp_number}")
            print(f"Course: {course_id}")
            print(f"Subject: {subject}")
            print(f"Date: {date}")
            print(f"Status: {matching_records[0]['Status']}")

            confirm = prompt(
                "Are you sure you want to delete this record?", ["Yes", "No"]
            )
            if confirm == "No":
                print("Deletion cancelled.")
                continue

            updated_records = [
                row
                for row in attendance_records
                if not (
                    row["TP_number"] == tp_number
                    and row["Date"] == date
                    and row["Subject"] == subject
                    and row["Course_id"] == course_id
                )
            ]

            write(updated_records, "../DATA/attendance.txt")
            print(
                f"Attendance record for {tp_number} in {subject} on {date} removed successfully."
            )

        elif choice == "Update attendance details":
            print_separator("Update Attendance")
            table("../DATA/attendance.txt")

            tp_number = input("Enter TP_number to update: ").strip().upper()
            date = input("Enter Date (YYYY-MM-DD) to update: ").strip()
            subject = input("Enter Subject to update: ").strip()

            attendance_records = get_all_rows("../DATA/attendance")

            matching_records = [
                row
                for row in attendance_records
                if row["TP_number"] == tp_number
                and row["Date"] == date
                and row["Subject"] == subject
            ]

            if not matching_records:
                print("Attendance record not found.")
                continue

            new_status = prompt("Select new Status", ["Present", "Absent", "Late"])

            updated = False
            for row in attendance_records:
                if (
                    row["TP_number"] == tp_number
                    and row["Date"] == date
                    and row["Subject"] == subject
                ):
                    row["Status"] = new_status
                    updated = True

            if updated:
                write(attendance_records, "../DATA/attendance.txt")
                print(
                    f"Attendance record for {tp_number} in {subject} on {date} updated to {new_status}."
                )
            else:
                print("Failed to update attendance record.")
