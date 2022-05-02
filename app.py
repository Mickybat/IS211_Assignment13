from flask import Flask
from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import flash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fa3*)NhM^g)M"nK'


def get_db_connection():
    conn = sqlite3.connect('hw13.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username or password'
        elif request.form['password'] != 'password':
            error = 'Invalid username or password'
        else:
            return redirect('/dashboard')

    return render_template("index.html", error=error)


@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    students = conn.execute('SELECT student_id, first_name, last_name FROM Students')
    quiz = conn.execute('SELECT quiz_id, subject, questions, quiz_date FROM Quizzes')
    return render_template('dashboard.html', students=students, quiz=quiz)


@app.route('/dashboard/student/<id>')
def show_student(id):
    conn = get_db_connection()
    students = conn.execute(f'SELECT student_id, first_name, last_name FROM Students where student_id = {id}')
    quiz = conn.execute(f'SELECT quiz_id, subject, questions, quiz_date FROM Quizzes where quiz_id = {id}')
    results = conn.execute(f'SELECT * from Results where student_id = {id}')

    return render_template('quiz_results.html', students=students, quiz=quiz, results=results)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if not first_name:
            flash('First name required!')
        elif not last_name:
            flash('Last name required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO Students (first_name, last_name) VALUES (?,?)', (first_name, last_name))
            conn.commit()
            conn.close()
            return redirect('/dashboard')
    return render_template('add_student.html')


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        questions = request.form['questions']
        date = request.form['quiz_date']
        if not subject:
            flash('Subject is required!')
        elif not questions:
            flash('Number of questions is required!')
        elif not date:
            flash('Date of quiz is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO Quizzes (subject, questions, quiz_date) VALUES (?,?,?)', (subject, questions, date))
            conn.commit()
            conn.close()
            return redirect('/dashboard')

    return render_template('add_quizzes.html')

@app.route('/results/add', methods=['GET', 'POST'])
def add_results():
    conn = get_db_connection()
    students = conn.execute(f'SELECT student_id, first_name, last_name FROM Students')
    quiz = conn.execute(f'SELECT quiz_id, subject, questions, quiz_date FROM Quizzes')
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        if not score:
            flash('MUST INSERT GRADE')
        elif not student_id:
            flash('must enter student id')
        elif not quiz_id:
            flash('must enter quiz id')
        else:
            conn.execute('INSERT INTO Results (student_id, quiz_id, score) VALUES (?,?,?)', (student_id, quiz_id, score))
            conn.commit()
            conn.close()
        return redirect('/dashboard')
    return render_template('add_results.html', students=students, quiz=quiz)


if __name__ == "__main__":
    app.run()
