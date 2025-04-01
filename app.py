from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        user_id TEXT UNIQUE,
                        password TEXT,
                        name TEXT,
                        email TEXT,
                        phone TEXT,
                        user_type TEXT,
                        photo TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bus_location (
                        id INTEGER PRIMARY KEY,
                        latitude REAL,
                        longitude REAL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        user_type = request.form['user_type']
        photo = 'images/default.jpg'

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, password, name, email, phone, user_type, photo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user_id, password, name, email, phone, user_type, photo))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user_id
        session['user_type'] = user[6]  # user_type is at index 6
        return redirect(url_for('dashboard'))
    return "Invalid credentials. Try again!"

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, photo FROM users WHERE user_type='driver'")
    driver = cursor.fetchone()
    conn.close()

    return render_template('dashboard.html', driver=driver)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/bus_location')
def bus_location():
    lat, lon = random.uniform(37.0, 38.0), random.uniform(-122.0, -121.0)
    return jsonify({'latitude': lat, 'longitude': lon})

if __name__ == '__main__':
    app.run(debug=True)
