def print_separator(title=""):
    width = 40
    print("\n" + "=" * width)
    if title:
        print(title.center(width))
    print("=" * width + "\n")


if __name__ == "__main__":
    print_separator()
