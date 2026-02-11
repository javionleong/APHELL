from FUNCTION.view_everything import view_all
from COMMON.prompt import *
from COMMON.design import *
from ADMINISTRATOR.administrator01 import admin_menu
from ADMINISTRATOR.administrator02 import student_management
from ADMINISTRATOR.administrator03 import course_management
from ADMINISTRATOR.administrator04 import class_schedule
from ADMINISTRATOR.administrator05 import report_generation


def administrator_main(user):
    while True:
        print_separator("Administrator Menu")

        choice = prompt(
            "Choose your choice",
            [
                "ADMIN MENU",
                "STUDENT MANAGEMENT MENU",
                "COURSE MANAGEMENT MENU",
                "CLASS SCHEDULE MANAGEMENT MENU",
                "REPORT GENERATION MENU",
                "View All",
                "Quit",
            ],
        )

        if choice == "Quit":
            exit()

        elif choice == "ADMIN MENU":
            admin_menu()

        elif choice == "STUDENT MANAGEMENT MENU":
            student_management()

        elif choice == "COURSE MANAGEMENT MENU":
            course_management()

        elif choice == "CLASS SCHEDULE MANAGEMENT MENU":
            class_schedule()

        elif choice == "REPORT GENERATION MENU":
            report_generation()

        elif choice == "View All":
            view_all(user)
