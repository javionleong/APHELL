from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def resource_allocation(user):
    print_separator("Resource Allocation")
    while True:
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all allocated resources",
                "Allocate new resource",
                "Update resource allocation",
                "Delete resource allocation",
                "Exit",
            ],
        )

        if choice == "QUIT" or choice == "Exit":
            print("Exiting Resource Allocation.")
            break

        elif choice == "View all allocated resources":
            print_separator("View all allocated resources")
            table("../DATA/resource.txt")

        elif choice == "Allocate new resource":
            existing_resource = get_all_rows("../DATA/resource")
            print_separator("Allocate New Resource")
            if existing_resource:
                existing_id = max(
                    int(res["Resource_id"][1:]) for res in existing_resource
                )
                resource_id = f"R{existing_id + 1}"
            else:
                resource_id = "R1"
            resource = input("Enter the classroom resource (e.g., Projector): ")
            room = prompt("Select the room:", ["Room A", "Room B"])
            status = prompt(
                "Select status:", ["Available", "Unavailable", "Maintenance"]
            )

            resource_allocate = {
                "Resource_id": resource_id,
                "Resource": resource,
                "Room": room,
                "Status": status,
            }
            add_row("../DATA/resource", resource_allocate)
            print("\nResource allocated successfully.")

        elif choice == "Update resource allocation":
            print_separator("Update Resource Allocation")
            resource_id = input("Enter the resource's ID to update: ")
            row = get_row("../DATA/resource", "Resource_id", resource_id)

            if not row:
                print(f"Resource ID: {resource_id} not found!")
            else:
                print("\nResource found:")
                print(", ".join(row.values()))
                print()

                updatable_fields = ["Resource", "Room", "Status"]
                update_field = prompt("Select field to update:", updatable_fields)

                if update_field == "Room":
                    new_value = prompt("Select the room:", ["Room A", "Room B"])
                elif update_field == "Status":
                    new_value = prompt(
                        "Select the status:",
                        ["Available", "Unavailable", "Maintenance"],
                    )
                else:
                    new_value = input(f"Enter new {update_field}: ")

                update_row(
                    "../DATA/resource",
                    "Resource_id",
                    resource_id,
                    update_field,
                    new_value,
                )
                print(
                    f"Resource allocation updated successfully! {update_field} changed to {new_value}"
                )

        elif choice == "Delete resource allocation":
            print_separator("Delete Resource Allocation")
            resource_id = input("Enter the resource ID to delete: ")
            row = get_row("../DATA/resource", "Resource_id", resource_id)

            if not row:
                print(f"Resource ID: {resource_id} not found!")
            else:
                print("\nClassroom resource found:")
                print(", ".join(row.values()))
                print()

                confirm = prompt(
                    f"Are you sure you want to delete the resource allocation for {resource_id}?",
                    ["Yes", "No"],
                )
                if confirm == "Yes":
                    delete_row("../DATA/resource", "Resource_id", resource_id)
                    print(f"Resource allocation for {resource_id} has been deleted.")
                else:
                    print("Deletion cancelled.")
