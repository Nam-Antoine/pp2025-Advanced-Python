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