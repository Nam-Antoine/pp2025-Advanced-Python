class Student:
    
    def __init__(self,name,id,dob):
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
    
    def set_name(self,name):
        self.__name = name
    def set_id(self,id):
        self.__id = id
    def set_dob(self, dob):
        self.__dob = dob
    
    @staticmethod
    def input():
        n = int(input("Enter number of students: "))
        print(f"number of students: {n}")
        students = []
        for i in range(n):
            name,id,dob = input(f"Enter student number {i} info: ").split()
            students.append(Student(name, id, dob))
        return students

    def list(self):
        print(f"{self.__name} - {self.__id} - {self.__dob}")

    def add_mark(self, course_id, mark):
        self.__mark[course_id] = mark

    def get_mark(self,course_id):
        return self.__mark.get(course_id)



class Course:
    def __init__(self,n,id):
        self.__name = n
        self.__id = id 

    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id
    
    def set_name(self,name):
        self.__name = name
    def set_id(self,id):
        self.__id = id

    @staticmethod
    def input():
        n = int(input("Enter the number of courses: "))
        print(f"The number of courses: {n}")
        courses = []
        for i in range(n):
            name,id = input("Enter course info: ").split()
            courses.append(Course(name,id))
        return courses
    
    def list(self):
        print(f"{self.__name} - {self.__id}")



class StudentMark:
    def __init__(self):
        self.__students = Student.input()
        self.__courses = Course.input()
    

    def display_student(self):
        for s in self.__students:
            s.list()

    def display_courses(self):
        for c in self.__courses:
            c.list()
        
    def input_mark(self):
        student_mark = []
        course_id = input("Enter course id: ")
        course = self.find_course_with_id(course_id)
        if not course:
            print(f"Course with {course_id} not found!")
            return
        
        for st in self.__students:
            mark = float(input(f"Enter mark for {st.get_name()} - {st.get_id()}: "))
            st.add_mark(course_id, mark)

    def find_course_with_id(self,course_id):
        for c in self.__courses:
            if c.get_id() == course_id:
                return c
        return None

    def show_mark(self):
        course_id = input("Enter course id: ")
        course = self.find_course_with_id(course_id)

        if not course:
            print(f"Course with {course_id} not found!")
            return
        
        print(f"\nMarks for {course.get_name()} ({course_id}):")
        has_Mark = False
        for st in self.__students:
            mark = st.get_mark(course_id)
            if mark is not None:
                has_Mark = True
                print(f"{st.get_name()} ({st.get_id()}): {mark}")
            else:
                print(f"{st.get_name()} ({st.get_id()}): No mark recorded")
        
        if not has_Mark:
            print("\nNo marks have been recorded for this course yet.")

    def run(self):
        while True:
            print("\n" + "="*50)
            print("STUDENT MARK MANAGEMENT SYSTEM")
            print("="*50)
            print("1. List all students")
            print("2. List all courses")
            print("3. Input marks for a course")
            print("4. Show marks for a course")
            print("5. Exit")
            
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
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    system = StudentMark()
    system.run()