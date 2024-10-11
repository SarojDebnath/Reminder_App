from flask import Flask, g, session, current_app
from .extensions import db, login_manager, mail
from .models import User
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Ensure the 'databases/' directory exists
    if not os.path.exists('databases'):
        os.makedirs('databases')
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Instead of before_first_request, use the app context to initialize the main database
    with app.app_context():
        db.create_all()  # Create tables for the main database (users)
    
    @app.before_request
    def set_user_database():
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                user_db = f'sqlite:///{os.path.join(app.root_path, "databases", user.username + ".db")}'
                app.config['SQLALCHEMY_DATABASE_URI'] = user_db
                db.engine.dispose()
                db.init_app(app)
                with app.app_context():
                    db.create_all()
    
    from .routes import routes
    app.register_blueprint(routes)
    
    return app
