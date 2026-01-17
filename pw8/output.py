#!/usr/bin/env python3
"""Output module for curses-based display"""

import curses

def display_menu(stdscr):
    """Display decorated menu using curses"""
    curses.curs_set(0)
    stdscr.clear()
    
    height, width = stdscr.getmaxyx()
    
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    stdscr.border()
    
    title = "=== STUDENT MANAGEMENT SYSTEM ==="
    stdscr.addstr(1, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
    
    menu = [
        "1. Input Students",
        "2. Input Courses",
        "3. Enter Marks for Course",
        "4. Show All Students",
        "5. Show All Courses",
        "6. Show Marks for Course",
        "7. Sort Students by GPA",
        "8. Exit"
    ]
    
    start_y = 4
    for i, option in enumerate(menu):
        stdscr.addstr(start_y + i, 5, option, curses.color_pair(2))
    
    stdscr.addstr(height - 2, 2, "Press any key to continue...", curses.color_pair(3))
    stdscr.refresh()
    stdscr.getch()

def display_students(stdscr, students):
    """Display students list with decoration"""
    stdscr.clear()
    stdscr.border()
    
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    height, width = stdscr.getmaxyx()
    
    title = "=== STUDENT LIST (Sorted by GPA) ==="
    stdscr.addstr(1, (width - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
    
    start_y = 3
    for i, s in enumerate(students):
        info = f"{s.get_name()} - {s.get_id()} - {s.get_dob()} - GPA: {s.calculate_gpa()}"
        if start_y + i < height - 2:
            stdscr.addstr(start_y + i, 2, info, curses.color_pair(2))
    
    stdscr.addstr(height - 2, 2, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()

def list_students(students):
    """List all students"""
    if not students:
        print("No students to display!")
        return
    
    print("\n=== Student List ===")
    for s in students:
        s.list()

def list_courses(courses):
    """List all courses"""
    if not courses:
        print("No courses to display!")
        return
    
    print("\n=== Course List ===")
    for c in courses:
        c.list()

def list_students_by_gpa(students):
    """List students sorted by GPA"""
    if not students:
        print("No students to display!")
        return
    
    sorted_students = sorted(students, key=lambda s: s.calculate_gpa(), reverse=True)
    print("\n=== Students Sorted by GPA ===")
    for s in sorted_students:
        s.list()
