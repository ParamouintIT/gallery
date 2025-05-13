from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
from extensions import db, login_manager, migrate

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///photogallery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)

# Configure CORS
CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})

# Import models
from models import User, Photo

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes
from routes import auth_bp, photos_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(photos_bp, url_prefix='/api/photos')

@app.route('/')
def index():
    return redirect('http://localhost:3000')

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow()})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True) 