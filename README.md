The Student Record System is a command-line application designed to manage student records efficiently. 
It allows users to create, read, update, and delete (CRUD) student records, as well as sort the records based on different criteria.
The system utilizes a linked list data structure to store student information, providing dynamic memory management and efficient data handling.
following are the funtionalities:
Add Student: Users can input student details (name, age, ID) to create a new record.
View Students: Users can view all student records or search for a specific student by ID.
Update Student: Users can update the details of an existing student record.
Delete Student: Users can delete a student record by providing the student's ID.
Sort Students: Users can sort the list of students by name or age.

we have used singly linked list to store student records. Each Node contains:
name: The name of the student.
age: The age of the student.
student_id: A unique identifier for the student.
next: A reference to the next node in the list.
The StudentList class manages the linked list and provides methods for all CRUD operations and sorting.
