"""API routes."""
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Document
from app.utils import allowed_file, generate_unique_filename, get_file_size, validate_pagination_params, sanitize_filename
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/documents', methods=['POST'])
def upload_document():
    """
    Upload a document.
    
    Returns:
        JSON response with document metadata or error message.
    """
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({
            'error': 'Invalid file type. Allowed types: PDF, TXT, DOCX'
        }), 400
    
    file_path = None
    try:
        # Sanitize and secure the original filename
        original_filename = file.filename
        safe_original = secure_filename(sanitize_filename(original_filename))
        
        # If sanitization results in empty or just extension, use a default
        if not safe_original or safe_original.startswith('.'):
            ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'txt'
            safe_original = f'document.{ext}'
        
        # Generate unique filename for storage
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Get file metadata
        file_size = get_file_size(file_path)
        file_type = original_filename.rsplit('.', 1)[1].lower()
        
        # Create database record
        document = Document(
            filename=unique_filename,
            original_filename=safe_original,
            file_size=file_size,
            file_type=file_type
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': document.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        # Clean up file if database operation fails
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@api_bp.route('/documents', methods=['GET'])
def list_documents():
    """
    List all documents with pagination.
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10, max: 100)
    
    Returns:
        JSON response with paginated document list.
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', current_app.config['DEFAULT_PAGE_SIZE'])
        page, per_page = validate_pagination_params(page, per_page)
        
        # Query documents with pagination
        pagination = db.paginate(
            db.select(Document).order_by(Document.upload_timestamp.desc()),
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        documents = [doc.to_dict() for doc in pagination.items]
        
        return jsonify({
            'documents': documents,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve documents: {str(e)}'}), 500

@api_bp.route('/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):
    """
    Retrieve a specific document by ID.
    
    Args:
        document_id (int): Document ID
    
    Returns:
        Document file or JSON error message.
    """
    try:
        # Query document using session.get()
        document = db.session.get(Document, document_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Check if file exists
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Document file not found'}), 404
        
        # Return file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=document.original_filename
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve document: {str(e)}'}), 500

@api_bp.route('/documents/<int:document_id>/metadata', methods=['GET'])
def get_document_metadata(document_id):
    """
    Retrieve document metadata without downloading the file.
    
    Args:
        document_id (int): Document ID
    
    Returns:
        JSON response with document metadata.
    """
    try:
        # Query document using session.get()
        document = db.session.get(Document, document_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        return jsonify({'document': document.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve metadata: {str(e)}'}), 500