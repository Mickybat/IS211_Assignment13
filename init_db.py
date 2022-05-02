import sqlite3

Students_TABLE = """ 
CREATE TABLE IF NOT EXISTS Students( 
    student_id integer PRIMARY KEY AUTOINCREMENT, 
    first_name TEXT, 
    last_name TEXT 
)
"""
Quizzes_TABLE = """
CREATE TABLE IF NOT EXISTS Quizzes( 
    quiz_id integer PRIMARY KEY AUTOINCREMENT, 
    subject TEXT, 
    questions integer, 
    quiz_date TEXT 
)
"""

QUIZ_RESULTS_TABLE = """ 
CREATE TABLE IF NOT EXISTS Results( 
    student_id integer,  
    quiz_id integer,
    score integer 
)
"""


def create_tables():
    conn = sqlite3.connect('hw13.db')

    cur = conn.cursor()
    cur.execute(Students_TABLE)
    cur.execute(Quizzes_TABLE)
    cur.execute(QUIZ_RESULTS_TABLE)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    create_tables()
