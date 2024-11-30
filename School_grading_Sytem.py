import mysql.connector

class GradingSystem:
    def __init__(self, name, student_id, grade, total_marks):
        self.name = name
        self.student_id = student_id
        self.grade = grade
        self.total_marks = total_marks
        
    def calculate_percentage(self):
       
        return (self.total_marks / 300) * 100

    def display_info(self):
        print(f"\nStudent Name: {self.name}")
        print(f"Student ID: {self.student_id}")
        print(f"Grade: {self.grade}")
        print(f"Total Marks: {self.total_marks}")
        print(f"Percentage: {self.calculate_percentage():.2f}%\n")


class MySQLDatabase:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def create_table(self, table_name):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            grade VARCHAR(255),
            total_marks INT,
            percentage DECIMAL(5, 2)
        )
        """
        self.cursor.execute(create_table_query)
        print(f"Table '{table_name}' checked or created.")

    def insert_student_data(self, name, student_id, grade, total_marks, percentage):
        query = "INSERT INTO students_details (name, id, grade, total_marks, percentage) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, student_id, grade, total_marks, percentage))
        self.connection.commit()
        print(f"Inserted student '{name}' into the database.")

    def check_student_id_exists(self, student_id):
        query = "SELECT COUNT(*) FROM students_details WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchone()[0] > 0

    def clear_student_data(self):
        query = "TRUNCATE TABLE students_details"
        self.cursor.execute(query)
        self.connection.commit()
        print("All student data cleared from the database.")

class StudentData:
    def __init__(self, database):
        self.database = database

    def add_student_data(self, name):
        name = name.upper()  

        while True:
            try:
                student_id = int(input("Enter the ID of the student: "))

                if self.database.check_student_id_exists(student_id):
                    print("Student ID already present. Change the student ID and try again.")
                    continue 

                grade = input("Enter the grade: ").upper()  
                marks = [int(input(f"Enter the marks for subject {i + 1}: ")) for i in range(3)]
                total_marks = sum(marks)
                percentage = round((total_marks / 300) * 100, 2)  

                self.database.insert_student_data(name, student_id, grade, total_marks, percentage)
                print("Student data added to the database.")
                break  

            except ValueError:
                print("Invalid input. Please enter numeric values for ID and marks.")

    def find_student_details(self, name):
        name = name.upper() 
        query = "SELECT id, grade, total_marks, percentage FROM students_details WHERE name = %s"
        self.database.cursor.execute(query, (name,))
        result = self.database.cursor.fetchone()

        if result:
            print(f"Data for {name} found.")
            student_id, grade, total_marks, percentage = result
            grading_system = GradingSystem(name, student_id, grade, total_marks)
            grading_system.display_info()
        else:
            print("Data not found.")
            if input("Do you want to add this student? (y/n): ").lower() == "y":
                self.add_student_data(name)

def main():
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'cdacacts'
    db_name = 'your_database'  

    database = MySQLDatabase(db_host, db_user, db_password, db_name)
    database.connect()
    database.create_table("students_details")

    student_data_manager = StudentData(database)

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Student Data")
        print("2. Find Student Data")
        print("3. Delete all student data")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                student_name = input("Enter the name of the student: ")
                student_data_manager.add_student_data(student_name)
            elif choice == 2:
                student_name = input("Enter the name of the student: ")
                student_data_manager.find_student_details(student_name)
            elif choice == 3:
                if input("Are you sure you want to clear all student data? (y/n): ").lower() == 'y':
                    database.clear_student_data()
            elif choice == 4:
                print("Goodbye")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    database.close()

if __name__ == "__main__":
    main()
import mysql.connector

class GradingSystem:
    def __init__(self, name, student_id, grade, total_marks):
        self.name = name
        self.student_id = student_id
        self.grade = grade
        self.total_marks = total_marks
        
    def calculate_percentage(self):
       
        return (self.total_marks / 300) * 100

    def display_info(self):
        print(f"\nStudent Name: {self.name}")
        print(f"Student ID: {self.student_id}")
        print(f"Grade: {self.grade}")
        print(f"Total Marks: {self.total_marks}")
        print(f"Percentage: {self.calculate_percentage():.2f}%\n")


class MySQLDatabase:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def create_table(self, table_name):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            grade VARCHAR(255),
            total_marks INT,
            percentage DECIMAL(5, 2)
        )
        """
        self.cursor.execute(create_table_query)
        print(f"Table '{table_name}' checked or created.")

    def insert_student_data(self, name, student_id, grade, total_marks, percentage):
        query = "INSERT INTO students_details (name, id, grade, total_marks, percentage) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, student_id, grade, total_marks, percentage))
        self.connection.commit()
        print(f"Inserted student '{name}' into the database.")

    def check_student_id_exists(self, student_id):
        query = "SELECT COUNT(*) FROM students_details WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchone()[0] > 0

    def clear_student_data(self):
        query = "TRUNCATE TABLE students_details"
        self.cursor.execute(query)
        self.connection.commit()
        print("All student data cleared from the database.")

class StudentData:
    def __init__(self, database):
        self.database = database

    def add_student_data(self, name):
        name = name.upper()  

        while True:
            try:
                student_id = int(input("Enter the ID of the student: "))

                if self.database.check_student_id_exists(student_id):
                    print("Student ID already present. Change the student ID and try again.")
                    continue 

                grade = input("Enter the grade: ").upper()  
                marks = [int(input(f"Enter the marks for subject {i + 1}: ")) for i in range(3)]
                total_marks = sum(marks)
                percentage = round((total_marks / 300) * 100, 2)  

                self.database.insert_student_data(name, student_id, grade, total_marks, percentage)
                print("Student data added to the database.")
                break  

            except ValueError:
                print("Invalid input. Please enter numeric values for ID and marks.")

    def find_student_details(self, name):
        name = name.upper() 
        query = "SELECT id, grade, total_marks, percentage FROM students_details WHERE name = %s"
        self.database.cursor.execute(query, (name,))
        result = self.database.cursor.fetchone()

        if result:
            print(f"Data for {name} found.")
            student_id, grade, total_marks, percentage = result
            grading_system = GradingSystem(name, student_id, grade, total_marks)
            grading_system.display_info()
        else:
            print("Data not found.")
            if input("Do you want to add this student? (y/n): ").lower() == "y":
                self.add_student_data(name)

def main():
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'cdacacts'
    db_name = 'your_database'  

    database = MySQLDatabase(db_host, db_user, db_password, db_name)
    database.connect()
    database.create_table("students_details")

    student_data_manager = StudentData(database)

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Student Data")
        print("2. Find Student Data")
        print("3. Delete all student data")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                student_name = input("Enter the name of the student: ")
                student_data_manager.add_student_data(student_name)
            elif choice == 2:
                student_name = input("Enter the name of the student: ")
                student_data_manager.find_student_details(student_name)
            elif choice == 3:
                if input("Are you sure you want to clear all student data? (y/n): ").lower() == 'y':
                    database.clear_student_data()
            elif choice == 4:
                print("Goodbye")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    database.close()

if __name__ == "__main__":
    main()
