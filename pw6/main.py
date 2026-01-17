
import curses
from curses import wrapper
import input as inp
import output as out
import os
import zipfile
import pickle

def load_data_from_archive():
    """Load data from students.dat using pickle"""
    if not os.path.exists("students.dat"):
        return None, None
    
    try:
        print("Loading data from students.dat...")
        
        # Extract files from zip
        with zipfile.ZipFile("students.dat", "r") as z:
            z.extractall()
        
        # Load using pickle
        students = None
        courses = None
        
        if os.path.exists("students.pkl"):
            with open("students.pkl", "rb") as f:
                students = pickle.load(f)
        
        if os.path.exists("courses.pkl"):
            with open("courses.pkl", "rb") as f:
                courses = pickle.load(f)
        
        if os.path.exists("marks.pkl"):
            with open("marks.pkl", "rb") as f:
                students = pickle.load(f)
        
        print("Data loaded successfully!")
        return students, courses
    except Exception as e:
        print(f"Error loading archive: {e}")
        return None, None


def compress_data():
    """Compress pickle files into students.dat"""
    print("\nSelect compression method:")
    print("1. ZIP (deflate)")
    print("2. ZIP (store - no compression)")
    choice = input("Choice (1 or 2): ").strip()
    
    try:
        files_to_compress = []
        if os.path.exists("students.pkl"):
            files_to_compress.append("students.pkl")
        if os.path.exists("courses.pkl"):
            files_to_compress.append("courses.pkl")
        if os.path.exists("marks.pkl"):
            files_to_compress.append("marks.pkl")
        
        if not files_to_compress:
            print("No files to compress!")
            return
        
        if choice == "1":
            with zipfile.ZipFile("students.dat", "w", zipfile.ZIP_DEFLATED) as z:
                for file in files_to_compress:
                    z.write(file)
            print("Pickle files compressed using ZIP (deflate) into students.dat")
        elif choice == "2":
            with zipfile.ZipFile("students.dat", "w", zipfile.ZIP_STORED) as z:
                for file in files_to_compress:
                    z.write(file)
            print("Pickle files compressed using ZIP (store) into students.dat")
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
            break


if __name__ == "__main__":
    """Entry point of the application"""
    wrapper(main_curses)
