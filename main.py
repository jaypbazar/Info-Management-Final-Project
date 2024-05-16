from flask import Flask, render_template, request
from backend import *

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/records/")
def records():
    return render_template('records.html')

@app.route("/students/", methods=["GET", "POST"])
def students():
    if request.method == 'GET':
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()

            conn.close()
            cursor.close()
            
            return render_template('students.html', students=rows)
    
    return render_template('students.html')

@app.route("/add_student/", methods=["GET", "POST"])
def add_student():
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
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()
            
            return render_template('students.html', students=rows)
            
    return render_template('students.html')

@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('students.html', students=rows)
            
    return render_template('students.html')

@app.route("/delete_student/<int:student_id>", methods=["GET", "POST"])
def delete_student(student_id):
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM students WHERE student_id={student_id}")
        
        # Update the displayed students
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()

        return render_template('students.html', students=rows)

@app.route("/instructors/", methods=["GET", "POST"])
def instructors():
    if request.method == 'GET':
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM instructors")
            rows = cursor.fetchall()

            conn.close()
            cursor.close()
            
            return render_template('instructors.html', instructors=rows)
    
    return render_template('instructors.html')

@app.route("/add_instructor/", methods=["GET", "POST"])
def add_instructor():
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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM instructors")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('instructors.html', instructors=rows)

    return render_template('instructors.html')

@app.route("/edit_instructor/<int:instructor_id>", methods=["GET", "POST"])
def edit_instructor(instructor_id):
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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM instructors")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('instructors.html', instructors=rows)

    return render_template('instructors.html')

@app.route("/delete_instructor/<int:instructor_id>")
def delete_instructor(instructor_id):
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM instructors WHERE instructor_id={instructor_id}")

        # Update the displayed instructors
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM instructors")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return render_template('instructors.html', instructors=rows)

@app.route("/grades/")
def grades():
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
    app.run(debug=True)
