#!/usr/bin/env python3

class Student:
    def __init__(self, id, name, dob):
        self.__id = id
        self.__name = name
        self.__dob = dob
        self.__marks = {}

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob

    def add_mark(self, course_id, mark):
        self.__marks[course_id] = mark

    def get_mark(self, course_id):
        return self.__marks.get(course_id)

    @staticmethod
    def input():
        n = int(input("Enter number of students: "))
        print(f"The number of students: {n}")
        students = []
        for i in range(n):
            name, id, dob = input(f"Enter info of student number {i+1}: ").split()
            students.append(Student(id, name, dob))
        return students

    def list(self):
        print(f"{self.__name} - {self.__id} - {self.__dob}")


class Course:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    def get_id(self): return self.__id
    def get_name(self): return self.__name

    @staticmethod
    def input():
        n = int(input("Enter number of courses: "))
        print(f"The number of courses: {n}")
        courses = []
        for i in range(n):
            name, id = input(f"Enter info of course number {i+1}: ").split()
            courses.append(Course(id, name))
        return courses

    def list(self):
        print(f"{self.__name} - {self.__id}")


def main():
    students = Student.input()
    courses = Course.input()

    course_id = input("Enter course id: ")
    if not any(c.get_id() == course_id for c in courses):
        print("Course not found.")
    else:
        for s in students:
            mark = float(input(f"Enter mark for {s.get_name()} - {s.get_id()}: "))
            s.add_mark(course_id, mark)

    for s in students:
        s.list()

    for c in courses:
        c.list()

    show_id = input("Enter course id: ")
    found = False
    for s in students:
        mark = s.get_mark(show_id)
        if mark is not None:
            print(f"{s.get_name()} - {s.get_id()}: {mark}")
            found = True
    if not found:
        print("No course found")


if __name__ == "__main__":
    main()