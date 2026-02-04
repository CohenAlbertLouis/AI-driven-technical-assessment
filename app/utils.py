"""Utility functions."""
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid
import unicodedata

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_file_extension(filename):
    """Extract file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def sanitize_filename(filename):
    """Sanitize filename to handle unicode and special characters."""
    # Normalize unicode characters
    filename = unicodedata.normalize('NFKD', filename)
    # Encode to ASCII, ignoring errors, then decode back
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    # If filename becomes empty after sanitization, use a default
    if not filename or filename == '.':
        filename = 'document'
    return filename

def generate_unique_filename(original_filename):
    """Generate a unique filename to avoid conflicts."""
    # First sanitize the filename
    sanitized = sanitize_filename(original_filename)
    # If sanitization removed everything, try to keep the extension at least
    ext = get_file_extension(original_filename)
    if not sanitized or sanitized == f'.{ext}':
        sanitized = f'document.{ext}'
    
    # Use secure_filename for additional security
    safe_name = secure_filename(sanitized)
    
    # Extract extension from the safe filename
    if '.' in safe_name:
        ext = safe_name.rsplit('.', 1)[1].lower()
    else:
        ext = get_file_extension(original_filename)
    
    # Generate unique name
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name

def get_file_size(file_path):
    """Get file size in bytes."""
    return os.path.getsize(file_path)

def validate_pagination_params(page, per_page):
    """Validate and sanitize pagination parameters."""
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else current_app.config['DEFAULT_PAGE_SIZE']
        
        # Ensure positive values
        page = max(1, page)
        per_page = max(1, min(per_page, current_app.config['MAX_PAGE_SIZE']))
        
        return page, per_page
    except (ValueError, TypeError):
        return 1, current_app.config['DEFAULT_PAGE_SIZE']