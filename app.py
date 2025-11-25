from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from models.final_emotion_model import FinalEmotionAnalyzer as EmotionAnalyzer
from utils.helpers import get_mental_health_suggestions

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'

# Initialize emotion analyzer
emotion_analyzer = EmotionAnalyzer()

# Database setup
def init_db():
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_analyses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  text_input TEXT,
                  emotion TEXT,
                  confidence REAL,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('database/users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database/users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Analyze emotion
    emotion, confidence = emotion_analyzer.analyze_emotion(text)
    suggestions = get_mental_health_suggestions(emotion)
    
    # Save analysis to database
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_analyses (user_id, text_input, emotion, confidence) VALUES (?, ?, ?, ?)",
             (session['user_id'], text, emotion, confidence))
    conn.commit()
    conn.close()
    
    return jsonify({
        'emotion': emotion,
        'confidence': round(confidence * 100, 2),
        'suggestions': suggestions
    })

@app.route('/history')
def get_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("SELECT text_input, emotion, confidence, timestamp FROM user_analyses WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10",
             (session['user_id'],))
    history = c.fetchall()
    conn.close()
    
    return jsonify([{
        'text': row[0][:100] + '...' if len(row[0]) > 100 else row[0],
        'emotion': row[1],
        'confidence': row[2],
        'timestamp': row[3]
    } for row in history])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)