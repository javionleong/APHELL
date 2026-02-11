from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def event_management(user):
    print_separator("Event Management")
    while True:
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all events",
                "Add a new event",
                "Update an event",
                "Delete an event",
                "Exit",
            ],
        )

        if choice == "QUIT" or choice == "Exit":
            print("Exiting event management.")
            break

        elif choice == "View all events":
            print_separator("View All Events")
            table("../DATA/events.txt")

        elif choice == "Add a new event":
            existing_event = get_all_rows("../DATA/events")
            print_separator("Add New Event")
            if existing_event:
                existing_id = max(int(eve["Event_id"][1:]) for eve in existing_event)
                event_id = f"E{existing_id + 1}"
            else:
                event_id = "E1"

            event = input("Enter the name of the event: ")
            date = input("Enter the date of the event (YYYY-MM-DD): ")
            venue = prompt(
                "Select an option:", ["Auditorium 1", "Auditorium 2", "APU Campus"]
            )

            conflict = any(
                eve.get("Event_id", "") == event_id
                or eve.get("Date", "") == date
                and eve.get("Venue", "") == venue
                for eve in existing_event
            )

            if conflict:
                print(
                    "Event ID already exist or the chosen Venue is already booked on the chosen Date"
                )
            else:
                event_detail = {
                    "Event_id": event_id,
                    "Event": event,
                    "Date": date,
                    "Venue": venue,
                }
                add_row("../DATA/events", event_detail)
                print("Event added successfully.")

        elif choice == "Update an event":
            print_separator("Update Event")
            event_id = input("Enter the event's ID to update: ")
            row = get_row("../DATA/events", "Event_id", event_id)

            if not row:
                print(f"Event ID: {event_id} not found!")
            else:
                print(f"Event found")
                print(", ".join(row.values()))
                print()

                updatable_fields = ["Event", "Date", "Venue"]
                update_field = prompt("Select field to update:", updatable_fields)

                if update_field == "Venue":
                    venue_choice = ["Auditorium 1", "Auditorium 2", "APU Campus"]
                    new_value = prompt("Select a venue:", venue_choice)
                elif update_field == "Date":
                    new_value = input("Enter new date (YYYY-MM-DD): ")
                elif update_field == "Event":
                    new_value = input(f"Enter new {update_field}: ")

                check_date = new_value if update_field == "Date" else row["Date"]
                check_venue = new_value if update_field == "Venue" else row["Venue"]
                check_event = new_value if update_field == "Event" else row["Event"]
                existing_event = get_all_rows("../DATA/events")
                conflict = any(
                    eve.get("Date", "") == check_date
                    and eve.get("Venue", "") == check_venue
                    and eve.get("Event", "") == check_event
                    for eve in existing_event
                )

                if conflict:
                    print("The chosen venue is already booked for the chosen date.")
                else:
                    update_row(
                        "../DATA/events",
                        "Event_id",
                        event_id,
                        update_field,
                        new_value,
                    )
                    print(
                        f"Event management updated successfully! {update_field} changed to {new_value}"
                    )

        elif choice == "Delete an event":
            print_separator("Delete Event")
            event_id = input("Enter the event's ID to delete: ")
            row = get_row("../DATA/events", "Event_id", event_id)

            if not row:
                print(f"Event ID: {event_id} not found!")
            else:
                print(f"Event found")
                print(", ".join(row.values()))
                print()

                confirm = prompt(
                    f"Are you sure you want to delete the event for {event_id}?",
                    ["Yes", "No"],
                )
                if confirm == "Yes":
                    delete_row("../DATA/events", "Event_id", event_id)
                    print(f"Event management for {event_id} has been deleted.")
                else:
                    print("Deletion cancelled.")
