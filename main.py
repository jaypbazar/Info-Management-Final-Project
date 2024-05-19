from flask import Flask, render_template, request
from backend import *

app = Flask(__name__)

@app.route("/")
def main():
    """
    The main function of the program. The first to be executed when running flask.

    Returns: 
        Render template function that renders the template argument specified ('index.html')
    """
    return render_template('index.html')

def update_records(conn):
    """
    A function that updates the contents of the records page. Executes the SELECT queries to 
    fetch the records from the database and pass it as an argument in render_template.

    Parameters:
        conn (mysql.connector.connection.MySQLConnection): The MySQL connection object.
        
    Returns:
        Render template function that renders the template argument specified ('records.html' along 
        with the variables students, courses, and grades) 
    """
    cursor = conn.cursor()
            
    cursor.execute("SELECT r.id, s.student_id, s.first_name, s.middle_name, s.last_name, s.suffix,c.course_id, c.course_name, r.grade, r.remark FROM students s, courses c, records r WHERE s.student_id = r.student_id AND c.course_id = r.course_id")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT * FROM students")
    rows2 = cursor.fetchall()
    
    cursor.execute("SELECT * FROM courses")
    rows3 = cursor.fetchall()
    
    cursor.execute("SELECT * FROM grades")
    rows4 = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('records.html', records=rows, students=rows2, courses=rows3, grades=rows4)

@app.route("/records/")
def records():
    """
    The function responsible in viewing the records table from the database. Calls the update_records 
    method to update the records in the records page.

    Returns:
        if there is connection from database:
            update_records method with parameter conn
        else: 
            render_template method with parameter 'records.html'
    """
    conn = connect()
    if conn is not None:
        return update_records(conn)
        
    return render_template('records.html')

@app.route("/add_record/", methods=["GET", "POST"])
def add_record():
    """
    The function responsible in adding new contents to the records table from the database. 
    Executes the INSERT query to add a record to the database. Also updates the content of
    the records page after successful insert.

    Returns:
        if there is connection from database and the request method is 'POST':
            update_records method with parameter conn
        else: 
            render_template method with parameter 'records.html'
    """
    if request.method == "POST":
        stud_id = request.form.get("StudentID")
        course_id = request.form.get("CourseID")
        grade = request.form.get("grade")
        remark = request.form.get("remark")
        
        conn = connect()
        if conn is not None:
            execute_query(conn, f"INSERT INTO records (student_id, course_id, grade, remark) VALUES ({stud_id}, '{course_id}', {grade}, '{remark}')")
            
            # Update the displayed records
            return update_records(conn)
            
    return render_template('records.html')

@app.route("/edit_record/<int:record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    """
    The function responsible in editing existing contents from the records table in the database. 
    Executes the UPDATE query to update a record from the database. Also updates the content of
    the records page after updating successfully.

    Parameters:
        record_id: The id of the record to be updated

    Returns:
        if there is connection from database and the request method is 'POST':
            update_records method with parameter conn
        else: 
            render_template method with parameter 'records.html'
    """
    if request.method == "POST":
        stud_id = request.form.get("StudentID")
        course_id = request.form.get("CourseID")
        grade = request.form.get("grade")
        remark = request.form.get("remark")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"UPDATE records SET student_id={stud_id}, course_id='{course_id}', grade={grade}, remark='{remark}' WHERE id={record_id}")

            # Update the displayed records
            return update_records(conn)
    
    return render_template('records.html')

@app.route("/delete_record/<int:record_id>")
def delete_record(record_id):
    """
    The function responsible in removing a content from the records table in the database. 
    Executes the DELETE query to remove a record from the database. Also updates the content of
    the records page after deleting successfully.

    Parameters:
        record_id: The id of the record to be removed

    Returns:
        if there is connection from database:
            update_records method with parameter conn
        else: 
            render_template method with parameter 'records.html'
    """
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM records WHERE id={record_id}")

        # Update the displayed records
        return update_records(conn)
  
    return render_template('records.html')

def update_students(conn):
    """
    A function that updates the contents of the students page. Executes the SELECT query to 
    fetch the students from the database and pass it as an argument in render_template.

    Parameters:
        conn (mysql.connector.connection.MySQLConnection): The MySQL connection object.
        
    Returns:
        Render template function that renders the template argument specified ('students.html' along 
        with the variable students) 
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY last_name")
    rows = cursor.fetchall()

    conn.close()
    cursor.close()

    return render_template('students.html', students=rows)

@app.route("/students/")
def students():
    """
    The function responsible in viewing the students table from the database. Calls the update_students 
    method to update the contents in the students page.

    Returns:
        if there is connection from database:
            update_students method with parameter conn
        else: 
            render_template method with parameter 'students.html'
    """
    conn = connect()
    if conn is not None:
        return update_students(conn)
    
    return render_template('students.html')

@app.route("/add_student/", methods=["GET", "POST"])
def add_student():
    """
    The function responsible in adding new contents to the students table from the database. 
    Executes the INSERT query to add a student to the database. Also updates the content of
    the students page after successful insert.

    Returns:
        if there is connection from database and the request method is 'POST':
            update_students method with parameter conn
        else: 
            render_template method with parameter 'students.html'
    """
    if request.method == "POST":
        stud_id = request.form.get("StudentID")
        firstname = request.form.get("firstName")
        middlename = request.form.get("middleName")
        lastname = request.form.get("lastName")
        suffix = request.form.get("suffix")
        age = request.form.get("age")
        email = request.form.get("email")
        
        conn = connect()
        if conn is not None:
            execute_query(conn, f"INSERT INTO students VALUES ({stud_id}, '{firstname}', '{middlename}', '{lastname}', '{suffix}', {age}, '{email}')")
            
            # Update the displayed students
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY last_name")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()
            
            return render_template('students.html', students=rows)
            
    return render_template('students.html')

@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    """
    The function responsible in editing existing contents from the students table in the database. 
    Executes the UPDATE query to update a student from the database. Also updates the content of
    the students page after updating successfully.

    Parameters:
        student_id: The id of the student to be updated

    Returns:
        if there is connection from database and the request method is 'POST':
            update_students method with parameter conn
        else: 
            render_template method with parameter 'students.html'
    """
    if request.method == "POST":
        stud_id = request.form.get("StudentID")
        firstname = request.form.get("firstName")
        middlename = request.form.get("middleName")
        lastname = request.form.get("lastName")
        suffix = request.form.get("suffix")
        age = request.form.get("age")
        email = request.form.get("email")
        
        conn = connect()
        if conn is not None:
            execute_query(conn, f"UPDATE students SET student_id={stud_id}, first_name='{firstname}', middle_name='{middlename}', last_name='{lastname}', suffix='{suffix}', age={age}, email='{email}' WHERE student_id={student_id}")

            # Update the displayed students
            return update_students(conn)
            
    return render_template('students.html')

@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    """
    The function responsible in removing a content from the students table in the database. 
    Executes the DELETE query to remove a student from the database. Also updates the content of
    the students page after deleting successfully.

    Parameters:
        student_id: The id of the student to be removed

    Returns:
        if there is connection from database:
            update_students method with parameter conn
        else: 
            render_template method with parameter 'students.html'
    """
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM students WHERE student_id={student_id}")
        
        # Update the displayed students
        return update_students(conn)
    
    return render_template('students.html')

def update_instructors(conn):
    """
    A function that updates the contents of the instructors page. Executes the SELECT query to 
    fetch the instructors from the database and pass it as an argument in render_template.

    Parameters:
        conn (mysql.connector.connection.MySQLConnection): The MySQL connection object.
        
    Returns:
        Render template function that renders the template argument specified ('instructors.html' along 
        with the variable instructors) 
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM instructors")
    rows = cursor.fetchall()

    conn.close()
    cursor.close()

    return render_template('instructors.html', instructors=rows)

@app.route("/instructors/")
def instructors():
    """
    The function responsible in viewing the instructors table from the database. Calls the 
    update_instructors method to update the contents in the instructors page.

    Returns:
        if there is connection from database:
            update_instructors method with parameter conn
        else: 
            render_template method with parameter 'instructors.html'
    """
    conn = connect()
    if conn is not None:
        return update_instructors(conn)
    
    return render_template('instructors.html')

@app.route("/add_instructor/", methods=["GET", "POST"])
def add_instructor():
    """
    The function responsible in adding new contents to the instructors table from the database. 
    Executes the INSERT query to add an instructor to the database. Also updates the content of
    the instructors page after successful insert.

    Returns:
        if there is connection from database and the request method is 'POST':
            update_instructors method with parameter conn
        else: 
            render_template method with parameter 'instructors.html'
    """
    if request.method == "POST":
        firstname = request.form.get("firstName")
        middlename = request.form.get("middleName")
        lastname = request.form.get("lastName")
        suffix = request.form.get("suffix")
        email = request.form.get("email")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"INSERT INTO instructors (first_name, middle_name, last_name, suffix, email) VALUES ('{firstname}', '{middlename}', '{lastname}', '{suffix}', '{email}')")

            # Update the displayed instructors
            return update_instructors(conn)

    return render_template('instructors.html')

@app.route("/edit_instructor/<int:instructor_id>", methods=["GET", "POST"])
def edit_instructor(instructor_id):
    """
    The function responsible in editing existing contents from the instructors table in the database. 
    Executes the UPDATE query to update an instructor from the database. Also updates the content of
    the instructors page after updating successfully.

    Parameters:
        instructor_id: The id of the instructor to be updated

    Returns:
        if there is connection from database and the request method is 'POST':
            update_instructors method with parameter conn
        else: 
            render_template method with parameter 'instructors.html'
    """
    if request.method == "POST":
        firstname = request.form.get("firstName")
        middlename = request.form.get("middleName")
        lastname = request.form.get("lastName")
        suffix = request.form.get("suffix")
        email = request.form.get("email")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"UPDATE instructors SET first_name='{firstname}', middle_name='{middlename}', last_name='{lastname}', suffix='{suffix}', email='{email}' WHERE instructor_id={instructor_id}")

            # Update the displayed instructors
            return update_instructors(conn)

    return render_template('instructors.html')

@app.route("/delete_instructor/<int:instructor_id>")
def delete_instructor(instructor_id):
    """
    The function responsible in removing a content from the instructors table in the database. 
    Executes the DELETE query to remove an instructor from the database. Also updates the content of
    the instructors page after deleting successfully.

    Parameters:
        instructor_id: The id of the instructor to be removed

    Returns:
        if there is connection from database:
            update_instructors method with parameter conn
        else: 
            render_template method with parameter 'instructors.html'
    """
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM instructors WHERE instructor_id={instructor_id}")

        # Update the displayed instructors
        return update_instructors(conn)
    
    return render_template('instructors.html')

def update_courses(conn):
    """
    A function that updates the contents of the courses page. Executes the SELECT queries to 
    fetch the courses and instructors from the database and pass it as an argument in 
    render_template.

    Parameters:
        conn (mysql.connector.connection.MySQLConnection): The MySQL connection object.
        
    Returns:
        Render template function that renders the template argument specified ('courses.html' 
        along with the variables courses and instructors)
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()

    cursor.execute("SELECT * FROM instructors")
    rows2 = cursor.fetchall()

    conn.close()
    cursor.close()
    
    return render_template('courses.html', courses=rows, instructors=rows2)

@app.route("/courses/")
def courses():
    """
    The function responsible in viewing the courses table from the database. Calls the 
    update_courses method to update the contents in the courses page.

    Returns:
        if there is connection from database:
            update_courses method with parameter conn
        else: 
            render_template method with parameter 'courses.html'
    """
    conn = connect()
    if conn is not None:
        return update_courses(conn)
    
    return render_template('courses.html')

@app.route("/add_course/", methods=["GET", "POST"])
def add_course():
    """
    The function responsible in adding new contents to the courses table from the database. 
    Executes the INSERT query to add a course to the database. Also updates the content of
    the courses page after successful insert.

    Returns:
        if there is connection from database and the request method is 'POST':
            update_courses method with parameter conn
        else: 
            render_template method with parameter 'courses.html'
    """
    if request.method == "POST":
        course_id = request.form.get("courseID")
        course_name = request.form.get("courseName")
        units = request.form.get("units")
        instructor_id = request.form.get("instructorID")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"INSERT INTO courses VALUES ('{course_id}', '{course_name}', {units}, {instructor_id})")

            # Update the displayed courses
            return update_courses(conn)
    
    return render_template('courses.html')

@app.route("/edit_course/<int:courseID>", methods=["GET", "POST"])
def edit_course(courseID):
    """
    The function responsible in editing existing contents from the courses table in the database. 
    Executes the UPDATE query to update a course from the database. Also updates the content of
    the courses page after updating successfully.

    Parameters:
        course_id: The id of the course to be updated

    Returns:
        if there is connection from database and the request method is 'POST':
            update_courses method with parameter conn
        else: 
            render_template method with parameter 'courses.html'
    """
    if request.method == "POST":
        course_id = request.form.get("courseID")
        course_name = request.form.get("courseName")
        units = request.form.get("units")
        instructor_id = request.form.get("instructorID")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"UPDATE courses SET course_id={course_id}, course_name='{course_name}', units={units}, instructor_id='{instructor_id}' WHERE course_id={courseID}")

            # Update the displayed courses
            return update_courses(conn)
    
    return render_template('courses.html')

@app.route("/delete_course/<int:courseID>")
def delete_course(courseID):
    """
    The function responsible in removing a content from the courses table in the database. 
    Executes the DELETE query to remove a course from the database. Also updates the content of
    the courses page after deleting successfully.

    Parameters:
        course_id: The id of the course to be removed

    Returns:
        if there is connection from database:
            update_courses method with parameter conn
        else: 
            render_template method with parameter 'courses.html'
    """
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM courses WHERE course_id={courseID}")

        # Update the displayed courses
        return update_courses(conn)

    return render_template('courses.html')

@app.route("/grades/")
def grades():
    """
    The function responsible in viewing the courses table from the database. Calls the 
    update_courses method to update the contents in the courses page.

    Returns:
        if there is connection from database:
            render_template method with parameter 'grades.html' and variable grades
        else: 
            render_template method with parameter 'grades.html' only
    """
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grades")
        rows = cursor.fetchall()
        
        conn.close()
        cursor.close()
        
        return render_template('grades.html', grades=rows)
    
    return render_template('grades.html')

if __name__ == '__main__':
    # Run flask upon program execution
    app.run(debug=True)
