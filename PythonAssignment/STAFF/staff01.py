from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def student_records(user):
    while True:
        print_separator("Student Records Management")
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View All Student Records",
                "Transfer A Student",
                "Withdraw A Student",
                "Exit",
            ],
        )

        if choice == "QUIT" or choice == "Exit":
            print("Exiting Student Records Management.")
            break

        elif choice == "View All Student Records":
            print_separator("View All Student Records")
            file_path = "../DATA/studentdetail.txt"
            table(file_path)

        elif choice == "Transfer A Student":
            print_separator("Transfer A Student")
            tp_number = input("Enter the transferring student's TP number: ")
            course_id = input(
                "Enter the course ID of the course the student is transferring to: "
            )
            course = input("Enter the course the student is transferring to: ")
            update_row(
                "../DATA/student_detail", "TP_number", tp_number, "Course_id", course_id
            )
            update_row(
                "../DATA/student_detail", "TP_number", tp_number, "Course", course
            )
            update_row(
                "../DATA/enrolment", "TP_number", tp_number, "Course_id", course_id
            )
            update_row("../DATA/enrolment", "TP_number", tp_number, "Course", course)
            print("Student is successfully transferred.")

        elif choice == "Withdraw A Student":
            print_separator("Withdraw A Student")
            tp_number = input("Enter the withdrawing student's TP number: ")
            delete_row("../DATA/student_detail", "TP_number", tp_number)
            delete_row("../DATA/enrolment", "TP_number", tp_number)
            delete_row("../DATA/user", "TP_number", tp_number)
            print("Student successfully withdrawn.")
