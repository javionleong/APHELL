from typing import List
from COMMON.query import get_all_rows, update_row, get_row


def prompt(question: str, options: List[str]) -> str:
    while True:
        print(question)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Please select a valid option.")
        except ValueError:
            print("Please select a valid option.")


def update_entity(entity_type, id_field, data_path):
    entities = get_all_rows(data_path)

    entity_id = input(
        f"Enter {id_field} of the {entity_type} to update (or 'QUIT' to cancel): "
    )
    if entity_id == "QUIT":
        return

    row = get_row(data_path, id_field, entity_id)

    if not row:
        print(f"{entity_type} with {id_field} {entity_id} not found!")
        return

    print(f"{entity_type} found: ", end="")
    for key, value in row.items():
        print(f"{key}: {value}", end=", ")
    print()

    updatable_fields = [key for key in row.keys() if key != id_field]
    updatable_fields.append("QUIT")

    update = prompt(f"Select field to update:", updatable_fields)
    if update == "QUIT":
        return

    new_value = input(f"Enter new {update} (or 'QUIT' to cancel): ")
    if new_value == "QUIT":
        return

    update_row(data_path, id_field, entity_id, update, new_value)

    print(
        f"{entity_type} {entity_id} updated successfully! {update} changed to {new_value}"
    )

    # question_ = "Do you confirm?"
    # options_ = ["Yes", "No"]
    # result = prompt(question_, options_)
    # print("You selected:", result)
