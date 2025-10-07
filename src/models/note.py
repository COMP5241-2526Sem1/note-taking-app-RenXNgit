from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from src.models.user import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # New optional fields
    tags = db.Column(db.Text, nullable=True)  # JSON encoded list of strings
    event_date = db.Column(db.Date, nullable=True)
    event_time = db.Column(db.Time, nullable=True)
    # position for ordering (lower = earlier/top)
    position = db.Column(db.Integer, nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.title}>'

    def to_dict(self):
        # decode tags JSON to list
        try:
            tags = json.loads(self.tags) if self.tags else []
        except Exception:
            tags = []

        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': tags,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'event_time': self.event_time.isoformat() if self.event_time else None,
            'position': self.position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

