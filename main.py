from flask import Flask, render_template
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
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * from students")
        rows = cursor.fetchall()
        
        return render_template('students.html', students=rows)
    
    return render_template('students.html')

@app.route("/instructors/")
def instructors():
    return render_template('instructors.html')

@app.route("/grades/")
def grades():
    return render_template('grades.html')

if __name__ == '__main__':
    app.run(debug=True)
