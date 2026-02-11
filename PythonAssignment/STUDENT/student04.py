"""
Module: student04.py
Description: Provides functionality for students to view their grades.
"""

from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def view_grade(user):
    """
    Retrieves and displays the grades for the student for their enrolled course.
    """
    # Read student details to determine the enrolled course.
    valid_login = read("../DATA/studentdetail.txt")
    for row in valid_login:
        if user["TP_number"] == row["TP_number"]:
            course_id = row["Course_id"]

    # Display header for grades tracking.
    print_separator("Grades Tracking")
    data = read("../DATA/grades.txt")
    grade_list = []
    # Filter grades that match the student's TP_number and course.
    for row in data:
        if user["TP_number"] == row["TP_number"] and course_id == row["Course_id"]:
            grade_list.append(row)
    data = grade_list
    selected_table(data)
