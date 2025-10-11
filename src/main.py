import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.note import Note

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Use environment variable for secret key, fallback to default for development
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Enable CORS for all routes
CORS(app)

# register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Use cloud database (PostgreSQL)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    # Handle SSL requirement for some PostgreSQL providers
    if DATABASE_URL.startswith('postgres'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {'sslmode': 'require'}
        }
else:
    # Fallback to SQLite for local development
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    # Lightweight migration: ensure new columns exist in SQLite table
    # If the columns are missing (older DB), add them using ALTER TABLE
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    cols = [c['name'] for c in inspector.get_columns('note')]
    with db.engine.connect() as conn:
        if 'tags' not in cols:
            conn.execute(text('ALTER TABLE note ADD COLUMN tags TEXT'))
        if 'event_date' not in cols:
            conn.execute(text('ALTER TABLE note ADD COLUMN event_date DATE'))
        if 'event_time' not in cols:
            conn.execute(text('ALTER TABLE note ADD COLUMN event_time TIME'))
        if 'position' not in cols:
            conn.execute(text('ALTER TABLE note ADD COLUMN position INTEGER'))
            # populate positions: set to rowid or incremental order
            # Fetch ids and set positions sequentially
            res = conn.execute(text('SELECT id FROM note ORDER BY updated_at DESC')).fetchall()
            for idx, row in enumerate(reversed(res), start=1):
                nid = row[0]
                conn.execute(text('UPDATE note SET position = :pos WHERE id = :id'), {'pos': idx, 'id': nid})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


# For Vercel serverless deployment
app_instance = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
