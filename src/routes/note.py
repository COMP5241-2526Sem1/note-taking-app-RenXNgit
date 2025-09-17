from flask import Blueprint, jsonify, request
from datetime import date, time
import json
from src.models.note import Note, db

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes ordered by position (if set) then most recently updated"""
    notes = Note.query.order_by(Note.position.asc().nullsfirst(), Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        # optional fields
        tags = data.get('tags')
        event_date = data.get('event_date')
        event_time = data.get('event_time')

        # ensure tags stored as JSON string
        tags_json = json.dumps(tags) if tags is not None else None

        # determine position: append to end (max position + 1)
        max_pos = db.session.query(db.func.max(Note.position)).scalar() or 0
        note = Note(
            title=data['title'],
            content=data['content'],
            tags=tags_json,
            event_date=event_date,
            event_time=event_time,
            position=(max_pos or 0) + 1
        )
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        # handle optional fields
        if 'tags' in data:
            note.tags = json.dumps(data.get('tags') or [])
        if 'event_date' in data:
            note.event_date = data.get('event_date')
        if 'event_time' in data:
            note.event_time = data.get('event_time')
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])


@note_bp.route('/notes/reorder', methods=['POST'])
def reorder_notes():
    """Accept a list of ids in desired order and persist position values"""
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({'error': 'Expected a list of note IDs'}), 400

        # Iterate and update positions
        for idx, nid in enumerate(data, start=1):
            note = Note.query.get(nid)
            if note:
                note.position = idx

        db.session.commit()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

