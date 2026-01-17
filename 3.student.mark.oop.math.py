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


class Course:
    def __init__(self, n, id, credit):
        self.__name = n
        self.__id = id
        self.__credit = credit

    def get_name(self):
        return self.__name
    
    def get_id(self):
        return self.__id
    
    def get_credit(self):
        return self.__credit
    
    def set_name(self, name):
        self.__name = name
    
    def set_id(self, id):
        self.__id = id
    
    def set_credit(self, credit):
        self.__credit = credit

    @staticmethod
    def input():
        n = int(input("Enter the number of courses: "))
        print(f"The number of courses: {n}")
        courses = []
        for i in range(n):
            name, id, credit = input(f"Enter course info (name id credit): ").split()
            courses.append(Course(name, id, float(credit)))
        return courses
    
    def list(self):
        print(f"{self.__name} - {self.__id} - Credits: {self.__credit}")


class StudentMark:
    def __init__(self):
        self.__students = Student.input()
        self.__courses = Course.input()
    
    def display_student(self, stdscr=None):
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, "ALL STUDENTS", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))
            row = 2
            for s in self.__students:
                stdscr.addstr(row, 0, f"{s.get_name()} - {s.get_id()} - {s.get_dob()}", curses.color_pair(1))
                row += 1
            stdscr.addstr(row + 1, 0, "Press any key to continue...", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getch()
        else:
            for s in self.__students:
                s.list()

    def display_student_by_gpa(self, stdscr=None):
        sorted_students = sorted(self.__students, key=lambda s: s.get_gpa(), reverse=True)
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, "STUDENTS SORTED BY GPA (DESCENDING)", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 70, curses.color_pair(2))
            row = 2
            for s in sorted_students:
                gpa = s.get_gpa()
                color = curses.color_pair(1) if gpa >= 3.5 else curses.color_pair(3) if gpa >= 3.0 else curses.color_pair(4)
                stdscr.addstr(row, 0, f"{s.get_name()} - {s.get_id()} - {s.get_dob()} | GPA: {gpa}", color)
                row += 1
            stdscr.addstr(row + 1, 0, "Press any key to continue...", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getch()
        else:
            print("\nStudents sorted by GPA (Descending):")
            print("-" * 60)
            for s in sorted_students:
                gpa = s.get_gpa()
                print(f"{s.get_name()} - {s.get_id()} - {s.get_dob()} | GPA: {gpa}")
            print("-" * 60)

    def display_courses(self, stdscr=None):
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, "ALL COURSES", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))
            row = 2
            for c in self.__courses:
                stdscr.addstr(row, 0, f"{c.get_name()} - {c.get_id()} - Credits: {c.get_credit()}", curses.color_pair(1))
                row += 1
            stdscr.addstr(row + 1, 0, "Press any key to continue...", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getch()
        else:
            for c in self.__courses:
                c.list()
        
    def input_mark(self, stdscr=None):
        if stdscr:
            # Curses mode - provide better UI
            stdscr.clear()
            stdscr.addstr(0, 0, "INPUT MARKS", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))
            
            # Show available courses
            stdscr.addstr(3, 0, "Available courses:", curses.color_pair(3))
            row = 4
            for c in self.__courses:
                stdscr.addstr(row, 2, f"{c.get_id()} - {c.get_name()} ({c.get_credit()} credits)", curses.color_pair(1))
                row += 1
            
            stdscr.addstr(row + 1, 0, "Enter course id: ", curses.color_pair(3))
            curses.echo()
            course_id = stdscr.getstr().decode('utf-8').strip()
            curses.noecho()
        else:
            course_id = input("Enter course id: ")
        
        course = self.find_course_with_id(course_id)
        if not course:
            if stdscr:
                stdscr.addstr(row + 3, 0, f"Course with {course_id} not found!", curses.color_pair(4))
                stdscr.addstr(row + 4, 0, "Press any key to continue...", curses.color_pair(3))
                stdscr.refresh()
                stdscr.getch()
            else:
                print(f"Course with {course_id} not found!")
            return
        
        credit = course.get_credit()
        
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, f"ENTERING MARKS FOR: {course.get_name()} ({course_id})", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))
            row = 3
            
        for st in self.__students:
            try:
                if stdscr:
                    stdscr.addstr(row, 0, f"Enter mark for {st.get_name()} ({st.get_id()}): ", curses.color_pair(1))
                    stdscr.refresh()
                    curses.echo()
                    mark = float(stdscr.getstr().decode('utf-8').strip())
                    curses.noecho()
                    row += 1
                else:
                    mark = float(input(f"Enter mark for {st.get_name()} - {st.get_id()}: "))
                
                st.add_mark(course_id, mark, credit)
            except ValueError:
                if stdscr:
                    stdscr.addstr(row, 0, "Invalid mark! Skipping this student.", curses.color_pair(4))
                    row += 1
                else:
                    print("Invalid mark! Skipping this student.")
        
        if stdscr:
            stdscr.addstr(row + 1, 0, "Marks recorded successfully!", curses.color_pair(2))
            stdscr.addstr(row + 2, 0, "Press any key to continue...", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getch()
        else:
            print("Marks recorded successfully!")

    def find_course_with_id(self, course_id):
        for c in self.__courses:
            if c.get_id() == course_id:
                return c
        return None

    def show_mark(self, stdscr=None):
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, "SHOW MARKS", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))
            
            # Show available courses
            stdscr.addstr(3, 0, "Available courses:", curses.color_pair(3))
            row = 4
            for c in self.__courses:
                stdscr.addstr(row, 2, f"{c.get_id()} - {c.get_name()}", curses.color_pair(1))
                row += 1
            
            stdscr.addstr(row + 1, 0, "Enter course id: ", curses.color_pair(3))
            curses.echo()
            course_id = stdscr.getstr().decode('utf-8').strip()
            curses.noecho()
        else:
            course_id = input("Enter course id: ")

        course = self.find_course_with_id(course_id)

        if not course:
            if stdscr:
                stdscr.addstr(row + 3, 0, f"Course with {course_id} not found!", curses.color_pair(4))
                stdscr.addstr(row + 4, 0, "Press any key to continue...", curses.color_pair(3))
                stdscr.refresh()
                stdscr.getch()
            else:
                print(f"Course with {course_id} not found!")
            return
        
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, f"MARKS FOR: {course.get_name()} ({course_id})", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * 60, curses.color_pair(2))
            row = 3
            has_mark = False
            
            for st in self.__students:
                mark = st.get_mark(course_id)
                if mark is not None:
                    has_mark = True
                    stdscr.addstr(row, 0, f"{st.get_name()} ({st.get_id()}): {mark}", curses.color_pair(1))
                else:
                    stdscr.addstr(row, 0, f"{st.get_name()} ({st.get_id()}): No mark recorded", curses.color_pair(3))
                row += 1
            
            if not has_mark:
                stdscr.addstr(row + 1, 0, "No marks have been recorded for this course yet.", curses.color_pair(4))
            
            stdscr.addstr(row + 2, 0, "Press any key to continue...", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getch()
        else:
            print(f"\nMarks for {course.get_name()} ({course_id}):")
            has_mark = False
            for st in self.__students:
                mark = st.get_mark(course_id)
                if mark is not None:
                    has_mark = True
                    print(f"{st.get_name()} ({st.get_id()}): {mark}")
                else:
                    print(f"{st.get_name()} ({st.get_id()}): No mark recorded")
            
            if not has_mark:
                print("\nNo marks have been recorded for this course yet.")

    def run(self, stdscr=None):
        if stdscr is None:
            # Fallback to non-curses version
            while True:
                print("\n" + "=" * 50)
                print("STUDENT MARK MANAGEMENT SYSTEM")
                print("=" * 50)
                print("1. List all students")
                print("2. List all courses")
                print("3. Input marks for a course")
                print("4. Show marks for a course")
                print("5. List students by GPA (Descending)")
                print("6. Exit")
                
                choice = input("\nEnter your choice: ")
                
                if choice == "1":
                    self.display_student()
                elif choice == "2":
                    self.display_courses()
                elif choice == "3":
                    self.input_mark()
                elif choice == "4":
                    self.show_mark()
                elif choice == "5":
                    self.display_student_by_gpa()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice! Please try again.")
        else:
            # Curses version
            curses.curs_set(0)
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
            
            while True:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                title = "STUDENT MARK MANAGEMENT SYSTEM"
                stdscr.addstr(0, (width - len(title)) // 2, title, curses.color_pair(5) | curses.A_BOLD)
                stdscr.addstr(1, 0, "=" * min(width - 1, 60), curses.color_pair(2))
                
                menu_items = [
                    "1. List all students",
                    "2. List all courses",
                    "3. Input marks for a course",
                    "4. Show marks for a course",
                    "5. List students by GPA (Descending)",
                    "6. Exit"
                ]
                
                for i, item in enumerate(menu_items, start=3):
                    stdscr.addstr(i, 2, item, curses.color_pair(1))
                
                stdscr.addstr(height - 2, 0, "Enter your choice: ", curses.color_pair(3))
                stdscr.refresh()
                
                choice = chr(stdscr.getch())
                
                if choice == "1":
                    self.display_student(stdscr)
                elif choice == "2":
                    self.display_courses(stdscr)
                elif choice == "3":
                    self.input_mark(stdscr)
                elif choice == "4":
                    self.show_mark(stdscr)
                elif choice == "5":
                    self.display_student_by_gpa(stdscr)
                elif choice == "6":
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Goodbye!", curses.color_pair(2) | curses.A_BOLD)
                    stdscr.refresh()
                    stdscr.getch()
                    break


if __name__ == "__main__":
    system = StudentMark()
    try:
        curses.wrapper(system.run)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Goodbye!")