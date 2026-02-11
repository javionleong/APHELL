from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def communication_menu(user):
    role = user["Role"]
    print_separator("Communication Menu")
    while True:
        role_choice = ["View messages", "Exit"]
        if role == "Staff":
            role_choice.insert(0, "Send a message")
            role_choice.insert(1, "Delete a message")
            role_choice.insert(2, "View all message")

        choice = prompt("Select an option (enter 'QUIT' to quit):", role_choice)

        if choice == "QUIT" or choice == "Exit":
            print("Exiting communication menu.")
            break

        elif choice == "Send a message":
            existing_msg = get_all_rows("../DATA/communications")
            print_separator("Send Message")
            receiver = prompt(
                "Select the receiver role:",
                ["Student", "Teacher", "Staff", "Administrator", "All"],
            )
            if existing_msg:
                existing_id = max(int(msg["Message_id"][1:]) for msg in existing_msg)
                message_id = f"M{existing_id + 1}"
            else:
                message_id = "M1"
            staff_name = input("Enter staff name: ")
            message = input("Enter the message to be sent: ")

            send_msg = {
                "Message_id": message_id,
                "Staff_name": staff_name,
                "Receiver": receiver,
                "Message": message,
            }
            add_row("../DATA/communications", send_msg)
            print("Message sent successfully.")

        elif choice == "View messages":
            print_separator("View Message")
            messages = get_all_rows("../DATA/communications")
            user_messages = [
                msg
                for msg in messages
                if msg["Receiver"] == role or msg["Receiver"] == "All"
            ]

            if not user_messages:
                print("There is no message for you.")
            else:
                print("Messages received:")
                for msg in user_messages:
                    print(f"From: {msg['Staff_name']} | Message: {msg['Message']}")

        elif choice == "Delete a message":
            print_separator("Delete A Message")
            message_id = input("Enter the message's ID you want to delete: ")
            row = get_row("../DATA/communications", "Message_id", message_id)

            if not row:
                print(f"Message ID: {message_id} not found!")
            else:
                print(f"Message found")
                print(", ".join(row.values()))
                print()

                confirm = prompt(
                    f"Are you sure you want to delete the message for {message_id}?",
                    ["Yes", "No"],
                )
                if confirm == "Yes":
                    delete_row("../DATA/communications", "Message_id", message_id)
                    print(f"Message for {message_id} has been deleted.")
                else:
                    print("Deletion cancelled.")

        elif choice == "View all message":
            print_separator("View All Message")
            table("../DATA/communication.txt")
