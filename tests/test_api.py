"""API endpoint tests."""
import pytest
import io
import os
from app.models import Document

class TestDocumentUpload:
    """Test document upload endpoint."""
    
    def test_upload_pdf_success(self, client):
        """Test successful PDF upload."""
        data = {
            'file': (io.BytesIO(b'PDF content here'), 'test.pdf')
        }
        response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert 'document' in json_data
        assert json_data['document']['file_type'] == 'pdf'
        assert json_data['document']['original_filename'] == 'test.pdf'
    
    def test_upload_txt_success(self, client):
        """Test successful TXT upload."""
        data = {
            'file': (io.BytesIO(b'Text content here'), 'test.txt')
        }
        response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['document']['file_type'] == 'txt'
    
    def test_upload_docx_success(self, client):
        """Test successful DOCX upload."""
        data = {
            'file': (io.BytesIO(b'DOCX content here'), 'test.docx')
        }
        response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['document']['file_type'] == 'docx'
    
    def test_upload_no_file(self, client):
        """Test upload without file."""
        response = client.post('/api/documents', data={}, content_type='multipart/form-data')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'No file provided' in json_data['error']
    
    def test_upload_empty_filename(self, client):
        """Test upload with empty filename."""
        data = {
            'file': (io.BytesIO(b'content'), '')
        }
        response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'No file selected' in json_data['error']
    
    def test_upload_invalid_file_type(self, client):
        """Test upload with invalid file type."""
        data = {
            'file': (io.BytesIO(b'content'), 'test.exe')
        }
        response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'Invalid file type' in json_data['error']

class TestDocumentList:
    """Test document listing endpoint."""
    
    def test_list_empty(self, client):
        """Test listing when no documents exist."""
        response = client.get('/api/documents')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'documents' in json_data
        assert len(json_data['documents']) == 0
        assert json_data['pagination']['total_items'] == 0
    
    def test_list_with_documents(self, client):
        """Test listing with uploaded documents."""
        # Upload test documents
        for i in range(3):
            data = {
                'file': (io.BytesIO(f'Content {i}'.encode()), f'test{i}.pdf')
            }
            client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        response = client.get('/api/documents')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data['documents']) == 3
        assert json_data['pagination']['total_items'] == 3
    
    def test_list_pagination(self, client):
        """Test pagination."""
        # Upload 5 documents
        for i in range(5):
            data = {
                'file': (io.BytesIO(f'Content {i}'.encode()), f'test{i}.txt')
            }
            client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        # Get first page with 2 items per page
        response = client.get('/api/documents?page=1&per_page=2')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert len(json_data['documents']) == 2
        assert json_data['pagination']['page'] == 1
        assert json_data['pagination']['per_page'] == 2
        assert json_data['pagination']['total_items'] == 5
        assert json_data['pagination']['total_pages'] == 3
        assert json_data['pagination']['has_next'] is True
        assert json_data['pagination']['has_prev'] is False
    
    def test_list_pagination_second_page(self, client):
        """Test second page of pagination."""
        # Upload 5 documents
        for i in range(5):
            data = {
                'file': (io.BytesIO(f'Content {i}'.encode()), f'test{i}.txt')
            }
            client.post('/api/documents', data=data, content_type='multipart/form-data')
        
        # Get second page
        response = client.get('/api/documents?page=2&per_page=2')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert len(json_data['documents']) == 2
        assert json_data['pagination']['has_next'] is True
        assert json_data['pagination']['has_prev'] is True

class TestDocumentRetrieval:
    """Test document retrieval endpoint."""
    
    def test_get_document_success(self, client):
        """Test successful document retrieval."""
        # Upload a document
        content = b'Test PDF content'
        data = {
            'file': (io.BytesIO(content), 'test.pdf')
        }
        upload_response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        document_id = upload_response.get_json()['document']['id']
        
        # Retrieve the document
        response = client.get(f'/api/documents/{document_id}')
        
        assert response.status_code == 200
        assert response.data == content
    
    def test_get_document_not_found(self, client):
        """Test retrieval of non-existent document."""
        response = client.get('/api/documents/9999')
        
        assert response.status_code == 404
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'not found' in json_data['error'].lower()
    
    def test_get_document_metadata(self, client):
        """Test metadata retrieval."""
        # Upload a document
        data = {
            'file': (io.BytesIO(b'Content'), 'test.txt')
        }
        upload_response = client.post('/api/documents', data=data, content_type='multipart/form-data')
        document_id = upload_response.get_json()['document']['id']
        
        # Get metadata
        response = client.get(f'/api/documents/{document_id}/metadata')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'document' in json_data
        assert json_data['document']['id'] == document_id
        assert json_data['document']['file_type'] == 'txt'
        assert 'upload_timestamp' in json_data['document']

class TestErrorHandling:
    """Test error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        json_data = response.get_json()
        assert 'error' in json_data