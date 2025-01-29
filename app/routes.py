from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User  # Import db and User model
from functools import wraps

bp = Blueprint('routes', __name__)

# Mock user database (replace with real database in production)
USERS = {
    'admin': 'password123'  # In production, hash passwords!
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@bp.route('/')
def index():
    return render_template('index.html', logged_in='username' in session)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('routes.home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Replace with real database query
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('routes.index'))

@bp.route('/home')
@login_required
def home():
    return render_template('home.html', username=session['username'])

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Assurez-vous que vous récupérez bien les données JSON
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Vérification de l'existence du nom d'utilisateur et de l'email
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 400

        # Créer un nouvel utilisateur (penser à hacher le mot de passe)
        new_user = User(username=username, email=email, password_hash=password)  # Hachage du mot de passe nécessaire
        db.session.add(new_user)

        try:
            db.session.commit()
            session['username'] = username
            return jsonify({'message': 'Registration successful'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Registration failed'}), 500
            
    return render_template('register.html')

# Error handlers
@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
