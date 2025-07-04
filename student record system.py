
import json
from datetime import datetime

class StudentNode:
    """Node class for student records linked list"""
    
    def __init__(self, student_id, name, grade, major):
        self.student_id = student_id
        self.name = name.strip().title()
        self.grade = grade.upper() if isinstance(grade, str) else grade
        self.major = major.strip().title()
        self.next = None
        self.added_date = datetime.now().strftime('%Y-%m-%d')
        
    def __str__(self):
        return (f"ID: {self.student_id} | {self.name:20} | "
                f"Grade: {self.grade} | Major: {self.major:15} | "
                f"Added: {self.added_date}")
    
    def to_dict(self):
        """Convert node data to dictionary for JSON serialization"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'grade': self.grade,
            'major': self.major,
            'added_date': self.added_date
        }

class StudentRecordSystem:
    """Linked list implementation for student records"""
    
    def __init__(self):
        self.head = None
        self._counter = 0
        self._setup()
        
    def _setup(self):
        """Initialize system and load data"""
        print("Initializing Student Record System...")
        try:
            with open('student_records.dat', 'r') as dbfile:
                data = json.load(dbfile)
                
                # Load records in reverse to maintain original order
                for record in reversed(data['records']):
                    self._add_node(
                        record['student_id'], 
                        record['name'],
                        record['grade'],
                        record['major'],
                        record['added_date']
                    )
                    
            print(f"Loaded {self._counter} existing records")
            self._sort_by_id()  # Re-sort after loading
            
        except (FileNotFoundError, json.JSONDecodeError):
            print("No existing database found. Starting fresh.")
    
    def _add_node(self, student_id, name, grade, major, added_date=None):
        """Internal method for adding nodes"""
        new_node = StudentNode(student_id, name, grade, major)
        if added_date:
            new_node.added_date = added_date
            
        new_node.next = self.head
        self.head = new_node
        self._counter += 1
        
    def _save_data(self):
        """Save current records to file"""
        records = []
        current = self.head
        
        while current:
            records.append(current.to_dict())
            current = current.next
            
        data = {'records': records}
        
        with open('student_records.dat', 'w') as dbfile:
            json.dump(data, dbfile, indent=2)
            
        print(f"\nDatabase saved with {len(records)} records")
    
    def _sort_by_id(self):
        """Sort records by student ID (insertion sort)"""
        if not self.head or not self.head.next:
            return
            
        sorted_head = None
        current = self.head
        
        while current:
            next_node = current.next
            if not sorted_head or sorted_head.student_id > current.student_id:
                current.next = sorted_head
                sorted_head = current
            else:
                temp = sorted_head
                while temp.next and temp.next.student_id < current.student_id:
                    temp = temp.next
                current.next = temp.next
                temp.next = current
            current = next_node
            
        self.head = sorted_head
    
    def _sort_by_name(self):
        """Sort records by student name (bubble sort)"""
        if not self.head or not self.head.next:
            return
            
        changed = True
        while changed:
            changed = False
            prev = None
            current = self.head
            
            while current.next:
                if current.name > current.next.name:
                    # Swap nodes
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                        
                    temp = current.next.next
                    current.next.next = current
                    current.next = temp
                    
                    prev = current.next
                    changed = True
                else:
                    prev = current
                    current = current.next
    
    def add_student(self):
        """Add a new student record"""
        print("\nAdd New Student")
        print("---------------")
        
        while True:
            student_id = input("Student ID: ").strip()
            if not student_id.isdigit():
                print("Error: ID must be numeric")
                continue
                
            # Check for duplicate ID
            current = self.head
            while current:
                if str(current.student_id) == student_id:
                    print(f"Error: Student ID {student_id} already exists")
                    break
                current = current.next
            else:
                break
                
        name = input("Full Name: ")
        while not name.strip():
            print("Error: Name cannot be empty")
            name = input("Full Name: ")
            
        grade = input("Grade (A-F or numeric): ").upper()
        major = input("Major: ") or "Undeclared"
        
        self._add_node(int(student_id), name, grade, major)
        print(f"\nStudent {name} added successfully!")
        self._save_data()
    
    def search_student(self, search_term):
        """Search for student by ID or name"""
        found = []
        current = self.head
        
        while current:
            if (str(search_term).lower() in current.name.lower() or 
                str(search_term).lower() in str(current.student_id)):
                found.append(current)
            current = current.next
            
        return found
    
    def update_student(self, student_id):
        """Update existing student record"""
        print("\nUpdate Student Record")
        print("---------------------")
        
        current = self.head
        while current:
            if str(current.student_id) == str(student_id):
                print(f"Current Record:\n{current}\n")
                
                # Update fields
                name = input(f"Name ({current.name}): ").strip()
                if name:
                    current.name = name.title()
                    
                grade = input(f"Grade ({current.grade}): ").strip().upper()
                if grade:
                    current.grade = grade
                    
                major = input(f"Major ({current.major}): ").strip()
                if major:
                    current.major = major.title()
                    
                print("\nRecord updated successfully!")
                self._save_data()
                return
                
            current = current.next
            
        print(f"Error: No student found with ID {student_id}")
    
    def delete_student(self, student_id):
        """Delete a student record"""
        previous = None
        current = self.head
        
        while current:
            if str(current.student_id) == str(student_id):
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                    
                print(f"\nDeleted record for {current.name} (ID: {current.student_id})")
                self._counter -= 1
                self._save_data()
                return
                
            previous = current
            current = current.next
            
        print(f"Error: No student found with ID {student_id}")
    
    def display_all(self, sort_by='id'):
        """Display all student records"""
        if not self.head:
            print("\nNo student records found")
            return
            
        if sort_by.lower() == 'name':
            self._sort_by_name()
            print("\nStudent Records (Sorted by Name)")
        else:
            self._sort_by_id()
            print("\nStudent Records (Sorted by ID)")
            
        print("=" * 80)
        current = self.head
        while current:
            print(current)
            current = current.next
            
        print(f"\nTotal records: {self._counter}")
    
    def export_to_text(self, filename="student_records.txt"):
        """Export records to text file"""
        if not self.head:
            print("No records to export")
            return
            
        with open(filename, 'w') as outfile:
            outfile.write("Student Records\n")
            outfile.write("=" * 50 + "\n")
            outfile.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            current = self.head
            while current:
                outfile.write(str(current) + "\n")
                current = current.next
                
        print(f"Records exported to {filename}")

def run_cli():
    """Command line interface for the system"""
    system = StudentRecordSystem()
    
    HELP_TEXT = """\nCommands:
    add      - Add new student
    search   - Search for student by ID/name
    update   - Update student record
    delete   - Delete student record
    display  - Display all records [id|name]
    export   - Export records to text file
    help     - Show this help
    exit     - Quit the program
    """
    
    print("\nWelcome to Student Record System")
    print(HELP_TEXT)
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'exit':
                print("Saving data...")
                system._save_data()
                print("Goodbye!")
                break
                
            elif cmd == 'help':
                print(HELP_TEXT)
                
            elif cmd == 'add':
                system.add_student()
                
            elif cmd.startswith('search'):
                term = input("Enter search term (ID or name): ").strip()
                if term:
                    results = system.search_student(term)
                    if results:
                        print("\nSearch Results:")
                        print("=" * 80)
                        for student in results:
                            print(student)
                        print(f"\nFound {len(results)} matching records")
                    else:
                        print("No matching records found")
                
            elif cmd.startswith('update'):
                student_id = input("Enter student ID to update: ").strip()
                if student_id:
                    system.update_student(student_id)
                
            elif cmd.startswith('delete'):
                student_id = input("Enter student ID to delete: ").strip()
                if student_id:
                    system.delete_student(student_id)
                
            elif cmd.startswith('display'):
                sort_by = 'id'
                parts = cmd.split()
                if len(parts) > 1 and parts[1] in ['id', 'name']:
                    sort_by = parts[1]
                system.display_all(sort_by)
                
            elif cmd == 'export':
                filename = input("Enter output filename [student_records.txt]: ").strip()
                system.export_to_text(filename or "student_records.txt")
                
            else:
                print("Invalid command. Type 'help' for options")
                
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit properly")
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == '__main__':
    run_cli()
