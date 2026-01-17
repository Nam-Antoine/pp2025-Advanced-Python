import math as m
import numpy as np
import curses


class Student:
    
    def __init__(self, name, id, dob):
        self.__name = name
        self.__id = id 
        self.__dob = dob
        self.__mark = {}

    # get + set method --> rule of thumb
    def get_name(self):
        return self.__name 
    
    def get_id(self):
        return self.__id
    
    def get_dob(self):
        return self.__dob
    
    def set_name(self, name):
        self.__name = name
    
    def set_id(self, id):
        self.__id = id
    
    def set_dob(self, dob):
        self.__dob = dob

    def add_mark(self, course_id, mark, credit):
        rounded_mark = m.floor(mark * 10) / 10
        self.__mark[course_id] = {'mark': rounded_mark, 'credit': credit}

    def get_mark(self, course_id):
        if course_id in self.__mark:
            return self.__mark[course_id]['mark']
        return None
    
    def cal_gpa(self):
        if not self.__mark:
            return 0.0
        
        marks = np.array([data['mark'] for data in self.__mark.values()])
        credits = np.array([data['credit'] for data in self.__mark.values()])

        total_credits = np.sum(credits)
        if total_credits == 0:
            return 0.0

        weighted_sum = np.sum(marks * credits)
        gpa = weighted_sum / total_credits
        return m.floor(gpa * 10) / 10

    @staticmethod
    def input():
        n = int(input("Enter number of students: "))
        print(f"number of students: {n}")
        students = []
        for i in range(n):
            name, id, dob = input(f"Enter student number {i} info: ").split()
            students.append(Student(name, id, dob))
        return students
    
    def list(self):
        gpa = self.cal_gpa()
        print(f"{self.__name} - {self.__id} - {self.__dob} - GPA: {gpa}")
    
    def get_gpa(self):
        return self.cal_gpa()