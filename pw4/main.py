
import curses
from curses import wrapper
import input as inp
import output as out

def main_curses(stdscr):
    """Main function with curses interface"""
    students = []
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
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")
        
        # Reinitialize curses
        stdscr = curses.initscr()


def main():
    """Entry point of the application"""
    wrapper(main_curses)


if __name__ == "__main__":
    main()
