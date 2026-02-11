from typing import Optional, Dict, List
from COMMON.csv import read, write


def get_all_rows(entity: str) -> List[Dict[str, str]]:
    return read(f"{entity}.txt")


def get_row(entity: str, key: str, value: str) -> Optional[Dict[str, str]]:
    data = get_all_rows(entity)
    for row in data:
        if row[key] == value:
            return row


def add_row(entity: str, row: Dict[str, str]) -> None:
    data = get_all_rows(entity)
    data.append(row)
    write(data, f"{entity}.txt")


def delete_row(entity: str, key: str, value: str) -> bool:
    data = get_all_rows(entity)
    updated_data = [row for row in data if row[key] != value]

    if len(updated_data) == len(data):
        print("User not found.")
        return False

    write(updated_data, f"{entity}.txt")
    print("User deleted successfully.")
    return True


def update_row(
    entity: str, key: str, value: str, updated_key: str, updated_value: str
) -> Optional[Dict[str, str]]:

    data = read(f"{entity}.txt")
    row = get_row(entity, key, value)

    for row in data:
        if row[key] == value:
            row[updated_key] = updated_value
            write(data, f"{entity}.txt")
