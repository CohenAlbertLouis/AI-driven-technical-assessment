"""Database models."""
from app import db
from datetime import datetime

class Document(db.Model):
    """Document model for storing file metadata."""
    
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    file_type = db.Column(db.String(10), nullable=False)  # pdf, txt, docx
    upload_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert document to dictionary."""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'upload_timestamp': self.upload_timestamp.isoformat()
        }
    
    def __repr__(self):
        return f'<Document {self.original_filename}>'