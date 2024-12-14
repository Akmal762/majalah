from flask import Flask, request, redirect, jsonify
from datetime import datetime
import sqlite3
from collections import Counter

app = Flask(__name__)

# Setup database
conn = sqlite3.connect('visitors.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    visit_time TEXT
)''')
conn.commit()

@app.route('/visit', methods=['GET'])
def visit():
    ip = request.remote_addr
    visit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO visits (ip, visit_time) VALUES (?, ?)", (ip, visit_time))
    conn.commit()
    return redirect('https://heyzine.com/flip-book/66c9d72848.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    cursor.execute("SELECT visit_time FROM visits")
    visits = cursor.fetchall()

    # Count visits per day
    visit_dates = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').date() for row in visits]
    visit_count = Counter(visit_dates)

    # Prepare JSON response
    response = [{"date": str(date), "count": count} for date, count in visit_count.items()]
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
