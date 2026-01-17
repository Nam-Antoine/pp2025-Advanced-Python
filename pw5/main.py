
import curses
from curses import wrapper
import input as inp
import output as out
import os
import zipfile

def load_data_from_archive():
    """Load data from students.dat if it exists"""
    from domains.student import Student
    from domains.course import Course
    
    if not os.path.exists("students.dat"):
        return None, None
    
    try:
        print("Loading data from students.dat...")
        
        # Extract files
        with zipfile.ZipFile("students.dat", "r") as z:
            z.extractall()
        
        # Load students
        students = []
        if os.path.exists("students.txt"):
            with open("students.txt", "r") as f:
                for line in f:
                    id, name, dob = line.strip().split(",")
                    students.append(Student(id, name, dob))
        
        # Load courses
        courses = []
        if os.path.exists("courses.txt"):
            with open("courses.txt", "r") as f:
                for line in f:
                    id, name, credit = line.strip().split(",")
                    courses.append(Course(id, name, int(credit)))
        
        # Load marks
        if os.path.exists("marks.txt"):
            with open("marks.txt", "r") as f:
                for line in f:
                    student_id, course_id, mark = line.strip().split(",")
                    for s in students:
                        if s.get_id() == student_id:
                            # Find the course to get credit
                            course = next((c for c in courses if c.get_id() == course_id), None)
                            if course:
                                s.add_mark(course_id, float(mark), course.get_credit())
                            break
        
        print("Data loaded successfully!")
        return students, courses
    except Exception as e:
        print(f"Error loading archive: {e}")
        return None, None


def compress_data():
    """Compress data files into students.dat"""
    print("\nSelect compression method:")
    print("1. ZIP (deflate)")
    print("2. ZIP (store - no compression)")
    choice = input("Choice (1 or 2): ").strip()
    
    try:
        files_to_compress = []
        if os.path.exists("students.txt"):
            files_to_compress.append("students.txt")
        if os.path.exists("courses.txt"):
            files_to_compress.append("courses.txt")
        if os.path.exists("marks.txt"):
            files_to_compress.append("marks.txt")
        
        if not files_to_compress:
            print("No files to compress!")
            return
        
        if choice == "1":
            with zipfile.ZipFile("students.dat", "w", zipfile.ZIP_DEFLATED) as z:
                for file in files_to_compress:
                    z.write(file)
            print("Files compressed using ZIP (deflate) into students.dat")
        elif choice == "2":
            with zipfile.ZipFile("students.dat", "w", zipfile.ZIP_STORED) as z:
                for file in files_to_compress:
                    z.write(file)
            print("Files compressed using ZIP (store) into students.dat")
        else:
            print("Invalid choice. Using ZIP deflate by default.")
            with zipfile.ZipFile("students.dat", "w", zipfile.ZIP_DEFLATED) as z:
                for file in files_to_compress:
                    z.write(file)
    except Exception as e:
        print(f"Error during compression: {e}")


def main_curses(stdscr):
    """Main function with curses interface"""
    # Try to load existing data
    students, courses = load_data_from_archive()
    
    if students is None:
        students = []
    if courses is None:
        courses = []
    
    while True:
        out.display_menu(stdscr)
        
        # Switch back to normal mode for input
        curses.endwin()
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            students = inp.input_students()
        elif choice == '2':
            courses = inp.input_courses()
        elif choice == '3':
            inp.input_marks(students, courses)
            input("Press Enter to continue...")
        elif choice == '4':
            if students:
                # Sort by GPA descending
                sorted_students = sorted(students, key=lambda s: s.calculate_gpa(), reverse=True)
                stdscr = curses.initscr()
                out.display_students(stdscr, sorted_students)
            else:
                print("No students to display!")
                input("Press Enter to continue...")
        elif choice == '5':
            out.list_courses(courses)
            input("Press Enter to continue...")
        elif choice == '6':
            inp.show_marks_for_course(students)
            input("Press Enter to continue...")
        elif choice == '7':
            out.list_students_by_gpa(students)
            input("Press Enter to continue...")
        elif choice == '8':
            print("\nExiting...")
            compress_data()
            print("Goodbye!")
        
        # Reinitialize curses
        stdscr = curses.initscr()


def main():
    """Entry point of the application"""
    wrapper(main_curses)


if __name__ == "__main__":
    main()
