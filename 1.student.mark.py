#Input functions
def student_number():
  n = int(input("Enter number of students: "))
  print(f"The number of students: {n}")
  return n

def student_info():
  n = student_number()
  students_list = []
  for i in range(n):
    name,id,DoB = input(f"Enter info of student number {i + 1}: ").split()
    students_list.append( {"name": name,"id": id,"DoB": DoB})
  return students_list

def course_number():
  c = int(input("Enter number of courses: "))
  print(f"The number of courses: {c}")
  return c

def course_info():
  c = course_number()
  courses_list = []
  for i in range(c):
    name,id = input(f"Enter info of course number {i + 1}: ").split()
    courses_list.append({"name": name, "id": id})
  return courses_list

students = student_info()
courses = course_info()
marks = {}

def input_mark():
  course_id = input("Enter course id: ")
  # if course_id not in courses["id"]:
  #   print("Course not found.")
  

  student_mark = []
  for student in students:
    mark = float(input(f"Enter mark for {student["name"]} - {student["id"]}: "))
    student_mark.append({"student_name": student["name"],"student_id": student["id"], "mark": mark})

  marks[course_id] = student_mark

input_mark()


#Listing function 
def listing_courses():
  for course in courses:
    print(f"{course["name"]} - {course["id"]}\n")
  
def listing_students():
  for student in students:
    print(f"{student["name"]} - {student["id"]} - {student["DoB"]}\nn")

def listing_mark():
    course_id = input("Enter course id: ")
    if course_id not in marks:
      print("No course found")

    for i in marks[course_id]:
      id = i["student_id"]
      mark = i["mark"]
      name = i["student_name"]
      print(f"{name} - {id}: {mark}")

listing_students()
listing_courses()

listing_mark()