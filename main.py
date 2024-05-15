from flask import Flask, render_template, request, redirect, session
from backend import read_db_config, connect, execute_query

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
    return render_template('add_student.html')

@app.route("/instructors/")
def instructors():
    return render_template('instructors.html')

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
