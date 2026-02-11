from typing import List, Dict


def read(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, "r") as file:
        lines = file.readlines()

    titles = lines[0].strip().split(",")

    data = []
    for line in lines[1:]:
        values = line.strip().split(",")
        row = {title: value for title, value in zip(titles, values)}
        data.append(row)

    return data


def write(data: List[Dict[str, str]], file_path: str) -> None:
    if not data:
        return

    with open(file_path, "w") as file:
        titles = data[0].keys()
        file.write(",".join(titles) + "\n")

        for row in data:
            file.write(",".join(str(row[key]) for key in titles) + "\n")


def table(file_path):
    data = read(file_path)

    if not data:
        print("Error: No data found in", file_path)
        return

    titles = list(data[0].keys())

    widths = [
        max(len(title), max(len(row.get(title, "")) for row in data))
        for title in titles
    ]

    header = "  ".join(f"{title:<{width}}" for title, width in zip(titles, widths))
    print(header)
    print("-" * sum(widths) + "--" * (len(titles) - 1))

    for row in data:
        row_str = "  ".join(
            f"{row.get(title, ''):<{width}}" for title, width in zip(titles, widths)
        )
        print(row_str)


def selected_table(data_in_list):

    data = data_in_list

    titles = list(data[0].keys())

    widths = [
        max(len(title), max(len(row.get(title, "")) for row in data))
        for title in titles
    ]

    header = "  ".join(f"{title:<{width}}" for title, width in zip(titles, widths))
    print(header)
    print("-" * sum(widths) + "--" * (len(titles) - 1))

    for row in data:
        row_str = "  ".join(
            f"{row.get(title, ''):<{width}}" for title, width in zip(titles, widths)
        )
        print(row_str)


if __name__ == "__main__":
    data = read("../DATA/user.txt")
    print(data)

    write(data, "../DATA/user.txt")
