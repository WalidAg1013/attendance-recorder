"""
Simple Student Attendance Management System
Student project: Python Programming Final Project
"""

import os
import datetime
import json

# ============================================================
# Data File Paths
# ============================================================
STUDENTS_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"

# ============================================================
# Color Codes for Console Output (Cross-platform compatible)
# ============================================================
class Colors:
    """ANSI color codes for terminal output formatting."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================
# Utility Functions
# ============================================================
def clear_screen():
    """Clear the console screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted section header.
    
    Args:
        title: The header title text to display
    """
    print(f"\n{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    """Print a success message in green."""
    print(f"{Colors.OKGREEN}[SUCCESS] {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message in red."""
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message in yellow."""
    print(f"{Colors.WARNING}[WARNING] {message}{Colors.ENDC}")

# ============================================================
# Data Persistence Functions
# ============================================================
def load_data(filename):
    """Load data from a JSON text file.
    
    Args:
        filename: Name of the file to load data from
        
    Returns:
        list: List of dictionaries containing the loaded data
    """
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            # Parse line-by-line JSON records
            records = []
            for line in content.split('\n'):
                if line.strip():
                    records.append(json.loads(line))
            return records
    except (json.JSONDecodeError, IOError) as e:
        print_error(f"Error loading data from {filename}: {e}")
        return []

def save_data(filename, records):
    """Save data records to a text file in JSON format.
    
    Args:
        filename: Name of the file to save data to
        records: List of dictionaries to save
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record) + '\n')
        return True
    except IOError as e:
        print_error(f"Error saving data to {filename}: {e}")
        return False

# ============================================================
# Student Management Functions
# ============================================================
def register_student():
    """Register a new student to the system.
    
    Prompts user for student details and validates input before saving.
    Checks for duplicate student IDs to prevent double registration.
    """
    print_header("REGISTER NEW STUDENT")
    
    students = load_data(STUDENTS_FILE)
    
    # Get student ID with validation
    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print_error("Student ID cannot be empty!")
        return
    
    # Check for duplicate ID
    for student in students:
        if student['student_id'] == student_id:
            print_error(f"Student ID '{student_id}' already exists!")
            return
    
    # Get student name with validation
    name = input("Enter Student Name: ").strip()
    if not name:
        print_error("Student name cannot be empty!")
        return
    
    # Get additional information
    class_name = input("Enter Class/Department (optional): ").strip()
    
    # Create student record
    student = {
        'student_id': student_id,
        'name': name,
        'class': class_name,
        'register_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    students.append(student)
    
    if save_data(STUDENTS_FILE, students):
        print_success(f"Student '{name}' (ID: {student_id}) registered successfully!")
    else:
        print_error("Failed to save student data!")

def view_all_students():
    """Display all registered students in a formatted table."""
    print_header("ALL REGISTERED STUDENTS")
    
    students = load_data(STUDENTS_FILE)
    
    if not students:
        print_warning("No students registered yet.")
        return
    
    # Print table header
    print(f"{'No.':<5} {'Student ID':<15} {'Name':<25} {'Class':<20} {'Register Date':<20}")
    print("-" * 90)
    
    # Print student records
    for idx, student in enumerate(students, 1):
        print(f"{idx:<5} {student['student_id']:<15} {student['name']:<25} "
              f"{student.get('class', 'N/A'):<20} {student['register_date']:<20}")
    
    print(f"\n{Colors.OKGREEN}Total students: {len(students)}{Colors.ENDC}")

def search_student():
    """Search for a student by ID or name."""
    print_header("SEARCH STUDENT")
    
    students = load_data(STUDENTS_FILE)
    
    if not students:
        print_warning("No students registered yet.")
        return
    
    keyword = input("Enter Student ID or Name to search: ").strip()
    if not keyword:
        print_error("Search keyword cannot be empty!")
        return
    
    # Search by ID or name (case-insensitive partial match)
    results = []
    for student in students:
        if (keyword.lower() in student['student_id'].lower() or 
            keyword.lower() in student['name'].lower()):
            results.append(student)
    
    if not results:
        print_warning(f"No student found matching '{keyword}'")
        return
    
    print(f"\n{Colors.OKGREEN}Found {len(results)} matching student(s):{Colors.ENDC}\n")
    print(f"{'Student ID':<15} {'Name':<25} {'Class':<20} {'Register Date':<20}")
    print("-" * 85)
    
    for student in results:
        print(f"{student['student_id']:<15} {student['name']:<25} "
              f"{student.get('class', 'N/A'):<20} {student['register_date']:<20}")

def delete_student():
    """Delete a student record by ID."""
    print_header("DELETE STUDENT")
    
    students = load_data(STUDENTS_FILE)
    
    if not students:
        print_warning("No students registered yet.")
        return
    
    student_id = input("Enter Student ID to delete: ").strip()
    if not student_id:
        print_error("Student ID cannot be empty!")
        return
    
    # Find and remove student
    for i, student in enumerate(students):
        if student['student_id'] == student_id:
            confirm = input(f"Are you sure you want to delete '{student['name']}'? (y/n): ").lower()
            if confirm == 'y':
                students.pop(i)
                # Also remove related attendance records
                attendance_records = load_data(ATTENDANCE_FILE)
                attendance_records = [r for r in attendance_records if r['student_id'] != student_id]
                save_data(ATTENDANCE_FILE, attendance_records)
                
                if save_data(STUDENTS_FILE, students):
                    print_success(f"Student '{student['name']}' deleted successfully!")
                else:
                    print_error("Failed to delete student!")
            else:
                print_warning("Deletion cancelled.")
            return
    
    print_error(f"Student ID '{student_id}' not found!")

# ============================================================
# Attendance Management Functions
# ============================================================
def mark_attendance():
    """Mark daily attendance for students.
    
    Allows bulk attendance marking with status options:
    P = Present, L = Late, A = Absent
    """
    print_header("MARK DAILY ATTENDANCE")
    
    students = load_data(STUDENTS_FILE)
    
    if not students:
        print_warning("No students registered. Please register students first.")
        return
    
    # Get attendance date
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    date_input = input(f"Enter date (YYYY-MM-DD) [default: {today}]: ").strip()
    attendance_date = date_input if date_input else today
    
    # Validate date format
    try:
        datetime.datetime.strptime(attendance_date, "%Y-%m-%d")
    except ValueError:
        print_error("Invalid date format! Please use YYYY-MM-DD.")
        return
    
    # Load existing records to check for duplicates
    attendance_records = load_data(ATTENDANCE_FILE)
    
    print(f"\n{Colors.BOLD}Marking attendance for: {attendance_date}{Colors.ENDC}")
    print(f"\nStatus options: {Colors.OKGREEN}P{Colors.ENDC}=Present, "
          f"{Colors.WARNING}L{Colors.ENDC}=Late, {Colors.FAIL}A{Colors.ENDC}=Absent, "
          f"{Colors.OKCYAN}S{Colors.ENDC}=Skip")
    print("-" * 60)
    
    new_records = []
    skipped = 0
    
    for student in students:
        student_id = student['student_id']
        name = student['name']
        
        # Check if attendance already recorded for this date
        already_recorded = False
        for record in attendance_records:
            if record['student_id'] == student_id and record['date'] == attendance_date:
                already_recorded = True
                break
        
        if already_recorded:
            print(f"{name:<30} {Colors.WARNING}[Already recorded]{Colors.ENDC}")
            continue
        
        # Get attendance status
        while True:
            status = input(f"{name:<30} (P/L/A/S): ").strip().upper()
            
            if status == 'S':
                skipped += 1
                break
            elif status in ['P', 'L', 'A']:
                status_map = {'P': 'Present', 'L': 'Late', 'A': 'Absent'}
                record = {
                    'student_id': student_id,
                    'name': name,
                    'date': attendance_date,
                    'status': status_map[status],
                    'record_time': datetime.datetime.now().strftime("%H:%M:%S")
                }
                new_records.append(record)
                break
            else:
                print_error("Invalid input! Please enter P, L, A, or S.")
    
    # Save new records
    if new_records:
        attendance_records.extend(new_records)
        if save_data(ATTENDANCE_FILE, attendance_records):
            print_success(f"\nAttendance recorded: {len(new_records)} student(s)")
            if skipped > 0:
                print_warning(f"Skipped: {skipped} student(s)")
        else:
            print_error("Failed to save attendance records!")
    else:
        if skipped == len(students):
            print_warning("All students were skipped. No records saved.")
        else:
            print_warning("No new attendance records to save.")

def view_attendance_records():
    """View attendance records with filtering options."""
    print_header("VIEW ATTENDANCE RECORDS")
    
    attendance_records = load_data(ATTENDANCE_FILE)
    
    if not attendance_records:
        print_warning("No attendance records found.")
        return
    
    print("Filter options:")
    print("  1. View all records")
    print("  2. View by student ID")
    print("  3. View by date")
    print("  4. View by date range")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    filtered_records = attendance_records
    
    if choice == '2':
        student_id = input("Enter Student ID: ").strip()
        filtered_records = [r for r in attendance_records if r['student_id'] == student_id]
        
    elif choice == '3':
        date = input("Enter date (YYYY-MM-DD): ").strip()
        filtered_records = [r for r in attendance_records if r['date'] == date]
        
    elif choice == '4':
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        filtered_records = [r for r in attendance_records 
                           if start_date <= r['date'] <= end_date]
    
    if not filtered_records:
        print_warning("No records match the filter criteria.")
        return
    
    # Sort records by date (newest first), then by student ID
    filtered_records.sort(key=lambda x: (x['date'], x['student_id']), reverse=True)
    
    # Display records
    print(f"\n{'No.':<5} {'Date':<12} {'Student ID':<12} {'Name':<20} {'Status':<10} {'Time':<10}")
    print("-" * 75)
    
    for idx, record in enumerate(filtered_records, 1):
        status = record['status']
        # Color-code status
        if status == 'Present':
            status_str = f"{Colors.OKGREEN}{status:<10}{Colors.ENDC}"
        elif status == 'Late':
            status_str = f"{Colors.WARNING}{status:<10}{Colors.ENDC}"
        else:
            status_str = f"{Colors.FAIL}{status:<10}{Colors.ENDC}"
        
        print(f"{idx:<5} {record['date']:<12} {record['student_id']:<12} "
              f"{record['name']:<20} {status_str} {record.get('record_time', 'N/A'):<10}")
    
    print(f"\n{Colors.OKGREEN}Total records: {len(filtered_records)}{Colors.ENDC}")

# ============================================================
# Statistics and Report Functions
# ============================================================
def attendance_statistics():
    """Generate attendance statistics with summary and details.
    
    Calculates attendance rates, identifies frequently absent students,
    and displays statistics in formatted tables.
    """
    print_header("ATTENDANCE STATISTICS")
    
    students = load_data(STUDENTS_FILE)
    attendance_records = load_data(ATTENDANCE_FILE)
    
    if not students:
        print_warning("No students registered yet.")
        return
    
    if not attendance_records:
        print_warning("No attendance records found.")
        return
    
    # Get date range
    dates = sorted(set(r['date'] for r in attendance_records))
    print(f"{Colors.BOLD}Report Period: {dates[0]} to {dates[-1]}{Colors.ENDC}")
    print(f"Total registered students: {len(students)}")
    print(f"Total attendance days recorded: {len(dates)}")
    
    # Overall statistics
    print_header("OVERALL STATISTICS")
    
    total_records = len(attendance_records)
    present_count = sum(1 for r in attendance_records if r['status'] == 'Present')
    late_count = sum(1 for r in attendance_records if r['status'] == 'Late')
    absent_count = sum(1 for r in attendance_records if r['status'] == 'Absent')
    
    print(f"{'Status':<15} {'Count':<10} {'Percentage':<15}")
    print("-" * 45)
    print(f"{'Present':<15} {present_count:<10} {present_count/total_records*100:.1f}%")
    print(f"{'Late':<15} {late_count:<10} {late_count/total_records*100:.1f}%")
    print(f"{'Absent':<15} {absent_count:<10} {absent_count/total_records*100:.1f}%")
    print("-" * 45)
    print(f"{'Total':<15} {total_records:<10} 100.0%")
    
    # Per-student statistics
    print_header("PER-STUDENT STATISTICS")
    
    print(f"{'Student ID':<12} {'Name':<20} {'Present':<8} {'Late':<8} {'Absent':<8} {'Rate':<8}")
    print("-" * 70)
    
    for student in students:
        sid = student['student_id']
        name = student['name']
        
        student_records = [r for r in attendance_records if r['student_id'] == sid]
        
        if not student_records:
            print(f"{sid:<12} {name:<20} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8}")
            continue
        
        s_present = sum(1 for r in student_records if r['status'] == 'Present')
        s_late = sum(1 for r in student_records if r['status'] == 'Late')
        s_absent = sum(1 for r in student_records if r['status'] == 'Absent')
        s_total = len(student_records)
        attendance_rate = s_present / s_total * 100
        
        rate_color = Colors.OKGREEN if attendance_rate >= 80 else Colors.WARNING if attendance_rate >= 60 else Colors.FAIL
        
        print(f"{sid:<12} {name:<20} {s_present:<8} {s_late:<8} {s_absent:<8} "
              f"{rate_color}{attendance_rate:.1f}%{Colors.ENDC}")
    
    # Identify at-risk students (attendance rate < 60%)
    print_header("AT-RISK STUDENTS (Attendance Rate < 60%)")
    
    at_risk = []
    for student in students:
        sid = student['student_id']
        student_records = [r for r in attendance_records if r['student_id'] == sid]
        
        if student_records:
            s_present = sum(1 for r in student_records if r['status'] == 'Present')
            rate = s_present / len(student_records) * 100
            if rate < 60:
                at_risk.append((student['name'], sid, rate))
    
    if at_risk:
        for name, sid, rate in at_risk:
            print(f"  {Colors.FAIL}{name} (ID: {sid}) - Rate: {rate:.1f}%{Colors.ENDC}")
    else:
        print(f"  {Colors.OKGREEN}No at-risk students found!{Colors.ENDC}")

def export_report():
    """Export attendance statistics report to a text file.
    
    Generates a comprehensive report with overall statistics,
    per-student breakdown, and at-risk student identification.
    """
    print_header("EXPORT STATISTICS REPORT")
    
    students = load_data(STUDENTS_FILE)
    attendance_records = load_data(ATTENDANCE_FILE)
    
    if not students or not attendance_records:
        print_warning("Insufficient data to generate report.")
        return
    
    # Generate report filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"attendance_report_{timestamp}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("       STUDENT ATTENDANCE MANAGEMENT SYSTEM - STATISTICS REPORT\n")
            f.write("=" * 70 + "\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Generated by: Student Attendance Management System\n")
            f.write("=" * 70 + "\n\n")
            
            # Report period
            dates = sorted(set(r['date'] for r in attendance_records))
            f.write("REPORT PERIOD\n")
            f.write("-" * 40 + "\n")
            f.write(f"From: {dates[0]}\n")
            f.write(f"To:   {dates[-1]}\n")
            f.write(f"Total registered students: {len(students)}\n")
            f.write(f"Total attendance days: {len(dates)}\n\n")
            
            # Overall statistics
            total_records = len(attendance_records)
            present_count = sum(1 for r in attendance_records if r['status'] == 'Present')
            late_count = sum(1 for r in attendance_records if r['status'] == 'Late')
            absent_count = sum(1 for r in attendance_records if r['status'] == 'Absent')
            
            f.write("OVERALL ATTENDANCE STATISTICS\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Status':<15} {'Count':<10} {'Percentage':<12}\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Present':<15} {present_count:<10} {present_count/total_records*100:.1f}%\n")
            f.write(f"{'Late':<15} {late_count:<10} {late_count/total_records*100:.1f}%\n")
            f.write(f"{'Absent':<15} {absent_count:<10} {absent_count/total_records*100:.1f}%\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Total':<15} {total_records:<10} 100.0%\n\n")
            
            # Per-student statistics
            f.write("PER-STUDENT ATTENDANCE BREAKDOWN\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Student ID':<12} {'Name':<20} {'Present':<8} {'Late':<8} {'Absent':<8} {'Rate':<8}\n")
            f.write("-" * 70 + "\n")
            
            for student in students:
                sid = student['student_id']
                name = student['name']
                student_records = [r for r in attendance_records if r['student_id'] == sid]
                
                if not student_records:
                    f.write(f"{sid:<12} {name:<20} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8}\n")
                    continue
                
                s_present = sum(1 for r in student_records if r['status'] == 'Present')
                s_late = sum(1 for r in student_records if r['status'] == 'Late')
                s_absent = sum(1 for r in student_records if r['status'] == 'Absent')
                s_total = len(student_records)
                attendance_rate = s_present / s_total * 100
                
                f.write(f"{sid:<12} {name:<20} {s_present:<8} {s_late:<8} {s_absent:<8} {attendance_rate:.1f}%\n")
            
            f.write("\n")
            
            # At-risk students
            f.write("AT-RISK STUDENTS (Attendance Rate < 60%)\n")
            f.write("-" * 40 + "\n")
            
            at_risk_found = False
            for student in students:
                sid = student['student_id']
                student_records = [r for r in attendance_records if r['student_id'] == sid]
                
                if student_records:
                    s_present = sum(1 for r in student_records if r['status'] == 'Present')
                    rate = s_present / len(student_records) * 100
                    if rate < 60:
                        f.write(f"  {student['name']} (ID: {sid}) - Rate: {rate:.1f}%\n")
                        at_risk_found = True
            
            if not at_risk_found:
                f.write("  No at-risk students found.\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("                     END OF REPORT\n")
            f.write("=" * 70 + "\n")
        
        print_success(f"Report exported to: {report_file}")
        
    except IOError as e:
        print_error(f"Failed to export report: {e}")

# ============================================================
# Main Menu and Program Entry
# ============================================================
def print_main_menu():
    """Display the main menu with all available options."""
    print(f"\n{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}  STUDENT ATTENDANCE MANAGEMENT SYSTEM{Colors.ENDC}")
    print(f"{Colors.OKGREEN}  Student project: Python Programming Final Project{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}")
    print(f"\n{Colors.BOLD}  MAIN MENU{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}1.{Colors.ENDC} Register New Student")
    print(f"  {Colors.OKGREEN}2.{Colors.ENDC} View All Students")
    print(f"  {Colors.OKGREEN}3.{Colors.ENDC} Search Student")
    print(f"  {Colors.OKGREEN}4.{Colors.ENDC} Delete Student")
    print(f"  {Colors.OKGREEN}5.{Colors.ENDC} Mark Attendance")
    print(f"  {Colors.OKGREEN}6.{Colors.ENDC} View Attendance Records")
    print(f"  {Colors.OKGREEN}7.{Colors.ENDC} Attendance Statistics")
    print(f"  {Colors.OKGREEN}8.{Colors.ENDC} Export Statistics Report")
    print(f"  {Colors.FAIL}0.{Colors.ENDC} Exit System")
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}")

def main():
    """Main program entry point.
    
    Runs the attendance management system with a loop-based
    menu interface until user chooses to exit.
    """
    # Ensure data files exist
    for filename in [STUDENTS_FILE, ATTENDANCE_FILE]:
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                pass
    
    while True:
        clear_screen()
        print_main_menu()
        
        choice = input(f"\nEnter your choice (0-8): ").strip()
        
        if choice == '1':
            register_student()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            mark_attendance()
        elif choice == '6':
            view_attendance_records()
        elif choice == '7':
            attendance_statistics()
        elif choice == '8':
            export_report()
        elif choice == '0':
            print(f"\n{Colors.OKGREEN}Thank you for using Student Attendance Management System!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Goodbye!{Colors.ENDC}\n")
            break
        else:
            print_error("Invalid choice! Please enter a number between 0 and 8.")
        
        input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main()

