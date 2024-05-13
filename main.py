from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/records/")
def records():
    return render_template('records.html')

@app.route("/students")
def students():
    return render_template('students.html')

@app.route("/instructors")
def instructors():
    return render_template('instructors.html')

@app.route("/grades")
def grades():
    return render_template('grades.html')

if __name__ == '__main__':
    app.run()
