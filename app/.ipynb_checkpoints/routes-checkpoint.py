from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session # Add current_app here
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import User, Member
from datetime import datetime
from .notification import send_email_reminder

# Define a Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    else:
        return redirect(url_for('routes.login'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id  # Store the user's ID in the session
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Login failed. Check your username and password.')
    return render_template('login.html')


@routes.route('/dashboard')
@login_required
def dashboard():
    members = Member.query.all()
    return render_template('dashboard.html', members=members)


@routes.route('/add_member', methods=['POST'])
@login_required
def add_member():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
    
    new_member = Member(name=name, phone=phone, email=email, due_date=due_date)
    db.session.add(new_member)
    db.session.commit()
    
    # Call the email sending function here
    send_email_reminder(email, name, due_date)  # Pass the email, name, and due date
    
    flash('Member added successfully! A reminder email has been sent.', 'success')
    return redirect(url_for('routes.dashboard'))

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)  # Remove the user_id from the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.login'))
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('routes.register'))

        # Check if the username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('routes.register'))

        # Create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Create a new database for this user
        user_db = f'sqlite:///{os.path.join(current_app.root_path, "databases", username + ".db")}'
        current_app.config['SQLALCHEMY_DATABASE_URI'] = user_db
        db.create_all()  # Create tables for this user

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')



