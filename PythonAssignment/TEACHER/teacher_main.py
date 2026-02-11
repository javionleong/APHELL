from FUNCTION.view_everything import view_all
from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *
from TEACHER.teacher01 import course_management
from TEACHER.teacher02 import student_enrolment
from TEACHER.teacher03 import grade_management
from TEACHER.teacher04 import attendance_management
from TEACHER.teacher05 import report_generation


def teacher_main(user):

    while True:
        print_separator("Teacher Menu")
        choice = prompt(
            "Select an option:",
            [
                "Course Management",
                "Student Enrolment",
                "Grade Management",
                "Attendance Management",
                "Report Generation",
                "View All",
                "Exit",
            ],
        )

        if choice == "Exit":
            print("Logging out...")
            break
        elif choice == "Course Management":
            course_management(user)
        elif choice == "Student Enrolment":
            student_enrolment(user)
        elif choice == "Grade Management":
            grade_management(user)
        elif choice == "Attendance Management":
            attendance_management(user)
        elif choice == "Report Generation":
            report_generation(user)
        elif choice == "View All":
            view_all(user)
