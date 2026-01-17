#!/usr/bin/env python3
"""Input module for handling user inputs"""

import pickle
from domains.student import Student
from domains.course import Course

def input_students():
    """Input students from user and save using pickle"""
    n = int(input("Enter number of students: "))
    print(f"The number of students: {n}")
    students = []
    for i in range(n):
        name, id, dob = input(f"Enter info of student number {i+1}: ").split()
        students.append(Student(id, name, dob))
    
    # Save using pickle
    with open("students.pkl", "wb") as f:
        pickle.dump(students, f)
    print("Student info saved using pickle")
    
    return students

def input_courses():
    """Input courses from user and save using pickle"""
    n = int(input("Enter number of courses: "))
    print(f"The number of courses: {n}")
    courses = []
    for i in range(n):
        name, id, credit = input(f"Enter info of course number {i+1} (name id credit): ").split()
        courses.append(Course(id, name, int(credit)))
    
    # Save using pickle
    with open("courses.pkl", "wb") as f:
        pickle.dump(courses, f)
    print("Course info saved using pickle")
    
    return courses

def input_marks(students, courses):
    """Input marks for a specific course and save using pickle"""
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
    
    # Save using pickle
    with open("marks.pkl", "wb") as f:
        pickle.dump(students, f)
    print("Marks saved using pickle")
    print("Marks entered successfully!")

def show_marks_for_course(students):
    """Show marks for a specific course"""
    show_id = input("Enter course id: ")
    found = False
    for s in students:
        mark = s.get_mark(show_id)
        if mark is not None:
            print(f"{s.get_name()} - {s.get_id()}: {mark}")
            found = True
    if not found:
        print("No marks found for this course")
