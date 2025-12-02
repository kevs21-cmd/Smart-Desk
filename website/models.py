from flask import session, logging
from flask_mysqldb import MySQL

mysql = MySQL()  # Ensure this matches your global app initialization

def get_all_students():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students")  # Fetch all students
        students = cursor.fetchall()
        cursor.close()  # Always close the cursor after use
        return students
    except Exception as e:
        logging.error(f"Database error: {e}")
        return []

def add_student(email, firstname, lastname, course, hashed_password):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO students (email, firstname, lastname, course, password) VALUES (%s, %s, %s, %s, %s)",
            (email, firstname, lastname, course, hashed_password)
        )
        mysql.connection.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        return True
    except Exception as e:
        logging.error(f"Database error: {e}")
        return False

def get_student_by_email(email):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        student = cursor.fetchone()
        cursor.close()  # Close the cursor
        return student
    except Exception as e:
        logging.error(f"Database error: {e}")
        return None

def get_logged_in_student():
    user_email = session.get('user_email')
    
    if not user_email:
        logging.debug('No user logged in. Session does not have user_email.')
        return None
    
    # Fetch the student details using the email
    student = get_student_by_email(user_email)
    
    if student:
        return student  # Return the student tuple if found
    else:
        logging.debug(f'No student found with email: {user_email}')
        return None
    
def get_student_by_id(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE id = %s", (user_id,))
        student = cursor.fetchone()  # Fetch the first matching student
        cursor.close()  # Close the cursor after use
        return student  # Returns the student if found, else None
    except Exception as e:
        logging.error(f"Database error: {e}")
        return None
    

    




