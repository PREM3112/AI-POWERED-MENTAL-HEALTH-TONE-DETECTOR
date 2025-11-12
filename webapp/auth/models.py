from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with mood history
    mood_entries = db.relationship('MoodHistory', backref='user', lazy=True)

class MoodHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text_input = db.Column(db.Text)
    emotion = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    input_type = db.Column(db.String(10))  # 'text' or 'speech'
    audio_filename = db.Column(db.String(200))  # Store audio file path if speech input
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'emotion': self.emotion,
            'confidence': self.confidence,
            'input_type': self.input_type,
            'created_at': self.created_at.isoformat()
        }