from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import User, Photo
from extensions import db
import os
import uuid
import mimetypes

auth_bp = Blueprint('auth', __name__)
photos_bp = Blueprint('photos', __name__)

# Authentication routes
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            login_user(user)
            return jsonify(user.to_dict())
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Photo routes
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@photos_bp.route('/')
@login_required
def get_photos():
    try:
        photos = Photo.query.filter_by(user_id=current_user.id).all()
        return jsonify([photo.to_dict() for photo in photos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/upload', methods=['POST'])
@login_required
def upload_photo():
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo provided'}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{extension}"
            
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Verify file type using mimetypes
            mime_type, _ = mimetypes.guess_type(filepath)
            if not mime_type or not mime_type.startswith('image/'):
                os.remove(filepath)
                return jsonify({'error': 'Invalid file type'}), 400
            
            photo = Photo(
                filename=filename,
                original_filename=original_filename,
                description=request.form.get('description', ''),
                user_id=current_user.id
            )
            
            db.session.add(photo)
            db.session.commit()
            
            return jsonify(photo.to_dict()), 201
        
        return jsonify({'error': 'File type not allowed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/<int:photo_id>')
@login_required
def get_photo(photo_id):
    try:
        photo = Photo.query.get_or_404(photo_id)
        if photo.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], photo.filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/<int:photo_id>', methods=['DELETE'])
@login_required
def delete_photo(photo_id):
    try:
        photo = Photo.query.get_or_404(photo_id)
        if photo.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(photo)
        db.session.commit()
        
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500 