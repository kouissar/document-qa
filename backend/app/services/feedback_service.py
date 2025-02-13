import sqlite3

DATABASE = 'feedback.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                response TEXT NOT NULL,
                feedback TEXT NOT NULL
            )
        ''')
        conn.commit()

def store_feedback(question: str, response: str, feedback: str):
    print(f"Storing feedback: Question: {question}, Response: {response}, Feedback: {feedback}")  # Debug log
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            INSERT INTO feedback (question, response, feedback)
            VALUES (?, ?, ?)
        ''', (question, response, feedback))
        conn.commit()

def get_all_feedback():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT question, response, feedback FROM feedback')
        results = cursor.fetchall()
        print("Fetched feedback:", results)  # Debug log
        return results 