"""
Module: student02.py
Description: Handles course enrolment functionality, including viewing courses and class schedules.
"""

from COMMON.csv import *
from COMMON.query import *
from COMMON.prompt import *
from COMMON.design import *


def course_enrollment(user):
    """
    Allows students to enroll in courses and view class schedules.
    """
    # Display header for course enrolment.
    print_separator("Course Enrolment")

    while True:
        # Prompt the user for enrolment options.
        user_choices = prompt(
            "Choose ur choices:", ["View Course", "View Class Schedules", "Quit"]
        )

        if user_choices == "Quit":
            break

        elif user_choices == "View Course":
            # Display available courses.
            print_separator("View Course")
            table("../DATA/course.txt")

        elif user_choices == "View Class Schedules":
            # Retrieve the student's enrolled course and group.
            reader = read("../DATA/enrolment.txt")
            for row in reader:
                if user["TP_number"] == row["TP_number"]:
                    course_id = row["Course_id"]
                    group = row["Group"]

            # Read class schedule data and filter by course and group.
            user_data = read("../DATA/class_schedule.txt")
            timetable_list = []
            for row in user_data:
                if course_id == row["Course_id"] and group == row["Group"]:
                    timetable_list.append(row)
            data = timetable_list
            selected_table(data)
