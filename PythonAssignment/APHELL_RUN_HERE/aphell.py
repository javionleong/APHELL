from COMMON.design import print_separator
from COMMON.query import *
from ADMINISTRATOR.administrator_main import administrator_main
from STUDENT.student_main import student_main
from STAFF.staff_main import staff_main
from TEACHER.teacher_main import teacher_main


def login():
    file_path = "../DATA/user.txt"
    users = read(file_path)
    print_separator("WELCOME APHELL")

    while True:
        tp_number = input("Enter TP Number: ")
        password = input("Enter Password: ")

        for user in users:
            if user["TP_number"] == tp_number and user["Password"] == password:
                print(f"Login successful! Welcome, {user['Name']} ({user['Role']}).")

                role = user["Role"].lower()
                if role == "student":
                    student_main(user)
                elif role == "teacher":
                    teacher_main(user)
                elif role == "staff":
                    staff_main(user)
                elif role == "administrator":
                    administrator_main(user)
                else:
                    print("Unknown role. Please contact the administrator.")
                    return None

                return user

        print("Invalid TP Number or Password. Please try again.\n")


if __name__ == "__main__":
    login()
