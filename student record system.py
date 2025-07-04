import json
from datetime import datetime

class StudentNode:
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
        return {
            'student_id': self.student_id,
            'name': self.name,
            'grade': self.grade,
            'major': self.major,
            'added_date': self.added_date
        }

class StudentRecordSystem:
    def __init__(self):
        self.head = None
        self._counter = 0
        self._load_existing_records()

    def _load_existing_records(self):
        print("Loading student records...")
        try:
            with open('student_records.dat', 'r') as f:
                data = json.load(f)
                for record in reversed(data.get('records', [])):
                    self._add_node(
                        record['student_id'],
                        record['name'],
                        record['grade'],
                        record['major'],
                        record['added_date']
                    )
            print(f"✔ Loaded {self._counter} record(s) from file.")
            self._sort_by_id()
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠ No previous data found. Starting fresh.")

    def _add_node(self, student_id, name, grade, major, added_date=None):
        node = StudentNode(student_id, name, grade, major)
        if added_date:
            node.added_date = added_date
        node.next = self.head
        self.head = node
        self._counter += 1

    def _save_data(self):
        records = []
        current = self.head
        while current:
            records.append(current.to_dict())
            current = current.next
        with open('student_records.dat', 'w') as f:
            json.dump({'records': records}, f, indent=2)
        print(f"[INFO] Saved {len(records)} record(s) to file.")

    def _sort_by_id(self):
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
        if not self.head or not self.head.next:
            return
        changed = True
        while changed:
            changed = False
            prev = None
            current = self.head
            while current.next:
                if current.name > current.next.name:
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
        print("\n[Add Student Record]")
        while True:
            student_id = input("Student ID: ").strip()
            if not student_id.isdigit():
                print("Please enter a valid numeric ID.")
                continue
            node = self.head
            while node:
                if str(node.student_id) == student_id:
                    print(f"Student ID {student_id} already exists.")
                    break
                node = node.next
            else:
                break
        name = input("Full Name: ").strip()
        while not name:
            print("Name cannot be empty.")
            name = input("Full Name: ").strip()
        grade = input("Grade (A-F or numeric): ").upper()
        major = input("Major: ") or "Undeclared"
        self._add_node(int(student_id), name, grade, major)
        print(f"✅ Student '{name}' added successfully.")
        self._save_data()

    def search_student(self, term):
        results = []
        current = self.head
        while current:
            if term.lower() in current.name.lower() or term == str(current.student_id):
                results.append(current)
            current = current.next
        return results

    def update_student(self, student_id):
        current = self.head
        while current:
            if str(current.student_id) == str(student_id):
                print(f"Current Record:\n{current}\n")
                name = input(f"Name ({current.name}): ").strip()
                if name:
                    current.name = name.title()
                grade = input(f"Grade ({current.grade}): ").strip().upper()
                if grade:
                    current.grade = grade
                major = input(f"Major ({current.major}): ").strip()
                if major:
                    current.major = major.title()
                print("✅ Record updated successfully.")
                self._save_data()
                return
            current = current.next
        print(f"❌ No student found with ID {student_id}")

    def delete_student(self, student_id):
        prev = None
        current = self.head
        while current:
            if str(current.student_id) == str(student_id):
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                print(f"🗑 Deleted record for {current.name} (ID: {current.student_id})")
                self._counter -= 1
                self._save_data()
                return
            prev = current
            current = current.next
        print(f"❌ No student found with ID {student_id}")

    def display_all(self, sort_by='id'):
        if not self.head:
            print("\nNo student records found.")
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
        if not self.head:
            print("No records to export.")
            return
        with open(filename, 'w') as f:
            f.write("Student Records\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            current = self.head
            while current:
                f.write(str(current) + "\n")
                current = current.next
        print(f"📁 Records exported to {filename}")

def run_cli():
    system = StudentRecordSystem()
    HELP = """
Commands:
  add      - Add a new student
  search   - Search student by ID or name
  update   - Update student details
  delete   - Delete student record
  display  - Display all records [id|name]
  export   - Export records to text file
  help     - Show commands
  exit     - Exit the program
"""
    print("\nWelcome to the Student Record Management System")
    print(HELP)
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            if cmd == 'exit':
                system._save_data()
                print("👋 Goodbye!")
                break
            elif cmd == 'help':
                print(HELP)
            elif cmd == 'add':
                system.add_student()
            elif cmd == 'search':
                term = input("Search by name or ID: ").strip()
                results = system.search_student(term)
                if results:
                    print("\nSearch Results:")
                    print("=" * 80)
                    for r in results:
                        print(r)
                else:
                    print("No matching records found.")
            elif cmd == 'update':
                student_id = input("Enter ID to update: ").strip()
                system.update_student(student_id)
            elif cmd == 'delete':
                student_id = input("Enter ID to delete: ").strip()
                system.delete_student(student_id)
            elif cmd.startswith('display'):
                _, *args = cmd.split()
                sort_key = args[0] if args else 'id'
                system.display_all(sort_key)
            elif cmd == 'export':
                filename = input("Filename [student_records.txt]: ").strip() or "student_records.txt"
                system.export_to_text(filename)
            else:
                print("Unknown command. Type 'help' for a list of commands.")
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit safely.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run_cli()
