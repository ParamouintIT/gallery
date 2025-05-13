# Photo Gallery Application

A full-stack web application for managing and displaying photos, built with Flask (backend) and React (frontend).

## Features

- User authentication (register, login, logout)
- Photo upload and management
- Gallery view with grid layout
- Secure file storage
- Responsive design

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- Flask-Login for authentication
- Flask-CORS for cross-origin requests
- SQLite database

### Frontend
- React
- TypeScript
- Material-UI
- React Router

## Setup

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask server:
```bash
python app.py
```
The backend will run on http://localhost:5001

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```
The frontend will run on http://localhost:3000

## Project Structure

```
photogallery/
├── app.py              # Flask application entry point
├── models.py           # Database models
├── routes.py           # API routes
├── extensions.py       # Flask extensions
├── requirements.txt    # Python dependencies
├── uploads/           # Photo storage directory
└── frontend/          # React frontend application
    ├── src/
    ├── public/
    └── package.json
```

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - User login
- GET /api/auth/logout - User logout

### Photos
- GET /api/photos/ - Get all photos for current user
- POST /api/photos/upload - Upload new photo
- GET /api/photos/<id> - Get specific photo
- DELETE /api/photos/<id> - Delete photo

## Development

The application uses SQLite for development. For production, consider using a more robust database like PostgreSQL.

## Security Features

- Secure password hashing
- Session-based authentication
- File type validation
- CORS protection
- Secure file naming 