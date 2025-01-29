from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    encrypted_email = db.Column(db.Text, nullable=True)
    email_iv = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-many relationship with encrypted data
    encrypted_data = db.relationship('EncryptedData', backref='user', lazy=True)

class EncryptedData(db.Model):
    __tablename__ = 'encrypted_data'
   
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)  # To identify different types of encrypted data
    encrypted_content = db.Column(db.Text, nullable=False)
    iv = db.Column(db.Text, nullable=False)  # Initialization vector for encryption
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)