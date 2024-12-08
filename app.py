import time
from datetime import datetime
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Подключение к MySQL
db_config = {
    "host": "mysqlhost",
    "user": "root",
    "password": "password",
    "database": "counter_db"
}

def get_db_connection():
    while True:
        try:
            return mysql.connector.connect(**db_config)
        except mysql.connector.Error as exc:
            time.sleep(0.5)
            continue

@app.route('/')
def hello():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Вставка данных в базу
    user_agent = request.headers.get('User-Agent')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO table_Counter (datetime, client_info) VALUES (%s, %s)",
        (now, user_agent)
    )
    conn.commit()

    # Получение количества запросов
    cursor.execute("SELECT COUNT(*) FROM table_Counter")
    count = cursor.fetchone()[0]

    # Получение времени последнего запроса
    cursor.execute("SELECT datetime FROM table_Counter ORDER BY datetime DESC LIMIT 1")
    last_request_time = cursor.fetchone()
    if last_request_time:
        last_request_time = last_request_time[0]
    else:
        last_request_time = "No requests yet."

    cursor.close()
    conn.close()

    return f'Hello World! I have been seen {count} times. Last request was made at {last_request_time}.\n'

@app.route('/stats')
def stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM table_Counter ORDER BY id DESC")
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)
