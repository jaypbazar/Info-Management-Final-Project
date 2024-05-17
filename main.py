from flask import Flask, render_template, request
from backend import *

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/records/")
def records():
    conn = connect()
    if conn is not None:
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
        
    return render_template('records.html')

@app.route("/add_record/", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        stud_id = request.form.get("StudentID")
        course_id = request.form.get("CourseID")
        grade = request.form.get("grade")
        remark = request.form.get("remark")
        
        conn = connect()
        if conn is not None:
            execute_query(conn, f"INSERT INTO records (student_id, course_id, grade, remark) VALUES ({stud_id}, '{course_id}', {grade}, '{remark}')")
            
            # Update the displayed records
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
            
    return render_template('records.html')

@app.route("/edit_record/<int:record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    if request.method == "POST":
        stud_id = request.form.get("StudentID")
        course_id = request.form.get("CourseID")
        grade = request.form.get("grade")
        remark = request.form.get("remark")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"UPDATE records SET student_id={stud_id}, course_id='{course_id}', grade={grade}, remark='{remark}' WHERE id={record_id}")

            # Update the displayed records
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
    
    return render_template('records.html')

@app.route("/delete_record/<int:record_id>")
def delete_record(record_id):
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM records WHERE id={record_id}")

        # Update the displayed records
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
  
    return render_template('records.html')

@app.route("/students/")
def students():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY last_name")
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
            cursor.execute("SELECT * FROM students ORDER BY last_name")
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
            cursor.execute("SELECT * FROM students ORDER BY last_name")
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
        cursor.execute("SELECT * FROM students ORDER BY last_name")
        rows = cursor.fetchall()
        cursor.close()

        return render_template('students.html', students=rows)
    
    return render_template('students.html')

@app.route("/instructors/")
def instructors():
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
    
    return render_template('instructors.html')

@app.route("/courses/")
def courses():
  conn = connect()
  if conn is not None:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()

    cursor.execute("SELECT * FROM instructors")
    rows2 = cursor.fetchall()

    conn.close()
    cursor.close()
    
    return render_template('courses.html', courses=rows, instructors=rows2)
  
  return render_template('courses.html')

@app.route("/add_course/", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_id = request.form.get("courseID")
        course_name = request.form.get("courseName")
        units = request.form.get("units")
        instructor_id = request.form.get("instructorID")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"INSERT INTO courses VALUES ('{course_id}', '{course_name}', {units}, {instructor_id})")

            # Update the displayed courses
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()

            cursor.execute("SELECT * FROM instructors")
            rows2 = cursor.fetchall()

            conn.close()
            cursor.close()
            
            return render_template('courses.html', courses=rows, instructors=rows2)
    
    return render_template('courses.html')

@app.route("/edit_course/<int:courseID>", methods=["GET", "POST"])
def edit_course(courseID):
    if request.method == "POST":
        course_id = request.form.get("courseID")
        course_name = request.form.get("courseName")
        units = request.form.get("units")
        instructor_id = request.form.get("instructorID")

        conn = connect()
        if conn is not None:
            execute_query(conn, f"UPDATE courses SET course_id={course_id}, course_name='{course_name}', units={units}, instructor_id='{instructor_id}' WHERE course_id={courseID}")

            # Update the displayed courses
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()

            cursor.execute("SELECT * FROM instructors")
            rows2 = cursor.fetchall()

            conn.close()
            cursor.close()
            
            return render_template('courses.html', courses=rows, instructors=rows2)
    
    return render_template('courses.html')

@app.route("/delete_course/<int:courseID>")
def delete_course(courseID):
    conn = connect()
    if conn is not None:
        execute_query(conn, f"DELETE FROM courses WHERE course_id={courseID}")

        # Update the displayed courses
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()

        cursor.execute("SELECT * FROM instructors")
        rows2 = cursor.fetchall()

        conn.close()
        cursor.close()
        
        return render_template('courses.html', courses=rows, instructors=rows2)

    return render_template('courses.html')

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
