from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def view_all(user):

    while True:
        print_separator("SEE SEE MENU")

        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "events",
                "communications",
                "resource",
                "feedback",
                "Exit",
            ],
        )

        if choice == "QUIT" or choice == "Exit":
            print_separator("Bye bye, System Administration")
            break
        elif choice == "events":
            print_separator("EVENTS")
            table("../DATA/events.txt")
        elif choice == "communications":

            print_separator("COMMUNICATIONS")

            role = read("../DATA/user.txt")

            found_role = False

            for row in role:
                if user["TP_number"] == row["TP_number"]:
                    user_role = user["Role"]
                    found_role = True

            if not found_role:
                print("TP number or Role not found.")
                break

            role_list = []

            reader = read("../DATA/communication.txt")

            found_message = False

            for row in reader:
                if row["Receiver"] == user_role or row["Receiver"] == "All":
                    role_list.append(row)
                    found_message = True

            if not found_message:
                print("You have no message.")
                break

            data = role_list

            selected_table(data)

        elif choice == "resource":
            print_separator("RESOURCE")
            table("../DATA/resource.txt")

        elif choice == "feedback":

            print_separator("FEEDBACK")

            reader = read("../DATA/feedback.txt")

            feedback_list = []

            found_feedback = False

            for row in reader:
                if user["TP_number"] == row["Receiver"]:
                    feedback_list.append(row)
                    found_feedback = True

            if not found_feedback:
                print("You have no feedback.")
                break

            data = feedback_list

            selected_table(data)

        else:
            print("Invalid choice. Please try again.")
