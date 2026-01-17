#!/usr/bin/env python3
"""Input module for handling user inputs"""

from domains.student import Student
from domains.course import Course

def input_students():
    """Input students from user and save to students.txt"""
    n = int(input("Enter number of students: "))
    print(f"The number of students: {n}")
    students = []
    for i in range(n):
        name, id, dob = input(f"Enter info of student number {i+1}: ").split()
        students.append(Student(id, name, dob))
    
    # Write to students.txt
    with open("students.txt", "w") as f:
        for s in students:
            f.write(f"{s.get_id()},{s.get_name()},{s.get_dob()}\n")
    print("Student info written to students.txt")
    
    return students

def input_courses():
    """Input courses from user and save to courses.txt"""
    n = int(input("Enter number of courses: "))
    print(f"The number of courses: {n}")
    courses = []
    for i in range(n):
        name, id, credit = input(f"Enter info of course number {i+1} (name id credit): ").split()
        courses.append(Course(id, name, int(credit)))
    
    # Write to courses.txt
    with open("courses.txt", "w") as f:
        for c in courses:
            f.write(f"{c.get_id()},{c.get_name()},{c.get_credit()}\n")
    print("Course info written to courses.txt")
    
    return courses

def input_marks(students, courses):
    """Input marks for a specific course and save to marks.txt"""
    if not courses:
        print("Please input courses first!")
        return
    if not students:
        print("Please input students first!")
        return
    
    course_id = input("Enter course id: ")
    course = next((c for c in courses if c.get_id() == course_id), None)
    if not course:
        print("Course not found.")
        return
    
    for s in students:
        mark = float(input(f"Enter mark for {s.get_name()} - {s.get_id()}: "))
        s.add_mark(course_id, mark, course.get_credit())
    
    # Write to marks.txt
    with open("marks.txt", "a") as f:
        for s in students:
            mark_data = s.get_mark(course_id)
            if mark_data is not None:
                f.write(f"{s.get_id()},{course_id},{mark_data}\n")
    print("Marks written to marks.txt")

