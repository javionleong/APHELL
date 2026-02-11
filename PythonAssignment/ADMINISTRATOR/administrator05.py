from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def report_generation():
    """Manage report generation for academic performance, attendance, and financial records."""

    while True:
        print_separator("REPORT GENERATION MENU")

        # Prompt admin to choose a report type
        choice = prompt(
            "Select an option (enter 'QUIT' to quit):",
            [
                "View all Academic Performance",
                "View all Attendance",
                "Financial",
                "Exit",
            ],
        )

        if choice in ["QUIT", "Exit"]:
            print_separator("\nBye bye, Admin\n")
            break

        elif choice == "View all Academic Performance":
            print_separator("ACADEMIC PERFORMANCE RECORDS")
            data = get_all_rows("../DATA/grades")

            if not data:
                print("No academic performance records found.")
                continue

            student_records = {}
            for row in data:
                tp_number = row["TP_number"]
                student_records.setdefault(tp_number, []).append(row)

            # Display academic performance per student
            for TP_number, records in student_records.items():
                print(
                    f"\n{'=' * 50}\n Academic Performance for Student: {TP_number}\n{'=' * 50}"
                )
                print(
                    f"{'Course ID':<10} | {'Assessment':<12} | {'Subject':<12} | {'Grade':<5} | Feedback"
                )
                print("-" * 70)

                for record in records:
                    print(
                        f"{record['Course_id']:<10} | {record['Assessment_type']:<12} | {record['Subject']:<12} | {record['Grade']:<5} | {record['Feedback']}"
                    )

                print("=" * 50)

        elif choice == "View all Attendance":
            print_separator("ATTENDANCE RECORDS")
            data = read("../DATA/attendance.txt")

            if not data:
                print("No attendance records found.")
                continue

            attendance_by_student = {}
            for row in data:
                tp_number = row["TP_number"]
                attendance_by_student.setdefault(tp_number, []).append(row)

            # Display attendance details per student
            for TP_number, records in attendance_by_student.items():
                total_classes = len(records)
                present_count = sum(
                    1 for row in records if row["Status"].lower() == "present"
                )
                attendance_percentage = (
                    (present_count / total_classes) * 100 if total_classes > 0 else 0
                )

                print(
                    f"\nAttendance for TP Number: {TP_number}  (Attendance: {attendance_percentage:.2f}%)\n"
                )
                print(f"{'Subject':<15} {'Date':<12} {'Status':<10}")
                print("=" * 40)

                for row in records:
                    print(f"{row['Subject']:<15} {row['Date']:<12} {row['Status']:<10}")

                print("=" * 40)

        elif choice == "Financial":
            while True:
                # Financial menu options
                financial_choice = prompt(
                    "Select an option:",
                    [
                        "View Financial Records",
                        "Update Financial Record",
                        "Delete Financial Record",
                        "Back",
                    ],
                )

                if financial_choice == "Back":
                    break

                elif financial_choice == "View Financial Records":
                    print_separator("FINANCIAL RECORDS")
                    table("../DATA/financial.txt")

                elif financial_choice == "Update Financial Record":
                    file_path = "../DATA/financial.txt"

                    # Read existing records
                    with open(file_path, "r") as file:
                        lines = file.readlines()

                    # Extract headers and data
                    headers = lines[0].strip().split(",")
                    records = [line.strip().split(",") for line in lines[1:]]

                    # Get user input
                    tp_number = input("Enter TP Number: ").strip()

                    updated_records = []
                    found = False

                    for record in records:
                        if record[0] == tp_number:  # Matching TP_number
                            found = True
                            tuition_fee = float(record[1])
                            amount_paid = float(record[2])
                            balance = float(record[3])

                            # Check if payment is already completed
                            if balance == 0:
                                print(
                                    "\nPayment is already completed for this student.\n"
                                )
                                return

                            # Ask for payment amount
                            amount = float(input("Enter amount to pay: "))

                            # Prevent overpayment
                            if amount > balance:
                                print(
                                    "\nError: Payment exceeds the required amount. Maximum you can pay is",
                                    balance,
                                    "\n",
                                )
                                return

                            # Update Amount Paid
                            new_amount_paid = amount_paid + amount

                            # Calculate new Balance
                            new_balance = tuition_fee - new_amount_paid

                            # Determine Payment Status
                            payment_status = (
                                "Completed" if new_balance == 0 else "Pending"
                            )

                            # Append updated record
                            updated_records.append(
                                [
                                    tp_number,
                                    tuition_fee,
                                    new_amount_paid,
                                    new_balance,
                                    payment_status,
                                ]
                            )

                            print("\nUpdated Payment Record for TP Number:", tp_number)
                            print(f"Previous Amount Paid: {amount_paid}")
                            print(f"New Amount Paid: {new_amount_paid}")
                            print(f"Remaining Balance: {new_balance}")

                            if new_balance == 0:
                                print("Done Payment. Payment is now completed.\n")
                            else:
                                print(f"Payment Status: {payment_status}\n")

                        else:
                            updated_records.append(record)

                    if not found:
                        print(f"\nError: TP Number {tp_number} not found in records.\n")
                        return

                    # Write updated records back to the file
                    with open(file_path, "w") as file:
                        file.write(",".join(headers) + "\n")  # Write header
                        for record in updated_records:
                            file.write(",".join(map(str, record)) + "\n")

                    print("Financial record updated successfully!\n")

                elif financial_choice == "Delete Financial Record":
                    # Prompt for TP Number to delete
                    tp_number = input("Enter TP Number to delete: ")
                    delete_row("../DATA/financial", "TP_number", tp_number)
                    print("Financial record deleted successfully!")
