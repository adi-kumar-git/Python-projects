import streamlit as st
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
        st.write(f"\nStudent Name: {self.name}")
        st.write(f"Student ID: {self.student_id}")
        st.write(f"Grade: {self.grade}")
        st.write(f"Total Marks: {self.total_marks}")
        st.write(f"Percentage: {self.calculate_percentage():.2f}%\n")


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
            st.success("Database connection established.")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            st.info("Database connection closed.")

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
        st.info(f"Table '{table_name}' checked or created.")

    def insert_student_data(self, name, student_id, grade, total_marks, percentage):
        query = "INSERT INTO students_details (name, id, grade, total_marks, percentage) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, student_id, grade, total_marks, percentage))
        self.connection.commit()
        st.success(f"Inserted student '{name}' into the database.")

    def check_student_id_exists(self, student_id):
        query = "SELECT COUNT(*) FROM students_details WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchone()[0] > 0

    def clear_student_data(self):
        query = "TRUNCATE TABLE students_details"
        self.cursor.execute(query)
        self.connection.commit()
        st.info("All student data cleared from the database.")

class StudentData:
    def __init__(self, database):
        self.database = database

    def add_student_data(self, name):
        name = name.upper()  

        student_id = st.number_input("Enter the ID of the student:", min_value=1, step=1)
        if self.database.check_student_id_exists(student_id):
            st.warning("Student ID already present. Change the student ID and try again.")
            return

        grade = st.text_input("Enter the grade:").upper()  
        marks = [st.number_input(f"Enter the marks for subject {i + 1}:", min_value=0, max_value=100, step=1) for i in range(3)]
        total_marks = sum(marks)
        percentage = round((total_marks / 300) * 100, 2)  

        if st.button("Add Student"):
            self.database.insert_student_data(name, student_id, grade, total_marks, percentage)
            st.success("Student data added to the database.")

    def find_student_details(self, name):
        name = name.upper() 
        query = "SELECT id, grade, total_marks, percentage FROM students_details WHERE name = %s"
        self.database.cursor.execute(query, (name,))
        result = self.database.cursor.fetchone()

        if result:
            st.success(f"Data for {name} found.")
            student_id, grade, total_marks, percentage = result
            grading_system = GradingSystem(name, student_id, grade, total_marks)
            grading_system.display_info()
        else:
            st.warning("Data not found.")
            if st.button("Add this student?"):
                self.add_student_data(name)

def main():
    st.title("Student Grading System")

    db_host = 'localhost'
    db_user = 'root'
    db_password = 'cdacacts'
    db_name = 'your_database'  

    database = MySQLDatabase(db_host, db_user, db_password, db_name)
    database.connect()
    database.create_table("students_details")

    student_data_manager = StudentData(database)

    menu = ["Add Student Data", "Find Student Data", "Delete all student data", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Student Data":
        student_name = st.text_input("Enter the name of the student:")
        if student_name:
            student_data_manager.add_student_data(student_name)

    elif choice == "Find Student Data":
        student_name = st.text_input("Enter the name of the student:")
        if student_name:
            student_data_manager.find_student_details(student_name)

    elif choice == "Delete all student data":
        if st.button("Clear All Data"):
            database.clear_student_data()

    elif choice == "Exit":
        st.write("Goodbye")
        database.close()
        st.stop()

if __name__ == "__main__":
    main()
