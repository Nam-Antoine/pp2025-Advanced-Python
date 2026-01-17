#!/usr/bin/env python3
"""Input module for handling user inputs"""

import pickle
from domains.student import Student
from domains.course import Course

# Global queue for background saves
save_queue = None

def set_save_queue(queue):
    """Set the queue for background saves"""
    global save_queue
    save_queue = queue

def input_students():
    """Input students from user and queue for pickle save"""
    n = int(input("Enter number of students: "))
    print(f"The number of students: {n}")
    students = []
    for i in range(n):
        name, id, dob = input(f"Enter info of student number {i+1}: ").split()
        students.append(Student(id, name, dob))
    
    # Queue for background save
    if save_queue:
        save_queue.put(('students', students))
        print("[Queued] Students will be saved in background")
    else:
        # Fallback to synchronous save
        with open("students.pkl", "wb") as f:
            pickle.dump(students, f)
        print("Student info saved using pickle")
    
    return students

def input_courses():
    """Input courses from user and queue for pickle save"""
    n = int(input("Enter number of courses: "))
    print(f"The number of courses: {n}")
    courses = []
    for i in range(n):
        name, id, credit = input(f"Enter info of course number {i+1} (name id credit): ").split()
        courses.append(Course(id, name, int(credit)))
    
    # Queue for background save
    if save_queue:
        save_queue.put(('courses', courses))
        print("[Queued] Courses will be saved in background")
    else:
        # Fallback to synchronous save
        with open("courses.pkl", "wb") as f:
            pickle.dump(courses, f)
        print("Course info saved using pickle")
    
    return courses

def input_marks(students, courses):
    """Input marks for a specific course and queue for pickle save"""
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
    
    # Queue for background save
    if save_queue:
        save_queue.put(('marks', students))
        print("[Queued] Marks will be saved in background")
    else:
        # Fallback to synchronous save
        with open("marks.pkl", "wb") as f:
            pickle.dump(students, f)
        print("Marks saved using pickle")
