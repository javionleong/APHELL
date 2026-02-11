from FUNCTION.view_everything import view_all
from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *
from STAFF.staff01 import *
from STAFF.staff02 import *
from STAFF.staff03 import *
from STAFF.staff04 import *
from STAFF.staff05 import *


def staff_main(user):

    while True:
        print_separator("Staff Menu")
        choice = prompt(
            "Select an option:",
            [
                "Student Records Management",
                "Timetable Management",
                "Resource Allocation",
                "Event Management",
                "Communication",
                "View All",
                "Exit",
            ],
        )

        if choice == "Exit":
            print("Logging out...")
            break
        elif choice == "Student Records Management":
            student_records(user)
        elif choice == "Timetable Management":
            timetable_management(user)
        elif choice == "Resource Allocation":
            resource_allocation(user)
        elif choice == "Event Management":
            event_management(user)
        elif choice == "Communication":
            communication_menu(user)
        elif choice == "View All":
            view_all(user)


if __name__ == "__main__":
    main()
