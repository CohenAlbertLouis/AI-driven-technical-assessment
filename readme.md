# Document Management REST API

A REST API built with Flask for managing document uploads (PDF, TXT, DOCX) with metadata storage, listing, and retrieval capabilities.

## Features

- ✅ Document upload (PDF, TXT, DOCX)
- ✅ Metadata storage (filename, size, type, timestamp)
- ✅ Document listing with pagination
- ✅ Document retrieval by ID
- ✅ Comprehensive error handling
- ✅ Unit tests with pytest

## Requirements

- Python 3.8+
- Flask 3.0.0
- SQLAlchemy
- pytest (for testing)

## Installation

1. Clone the repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### 1. Upload Document

**Endpoint:** `POST /api/documents`

**Description:** Upload a document (PDF, TXT, or DOCX)

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/documents \
  -F "file=@/path/to/document.pdf"
```

**Response (201 Created):**
```json
{
  "message": "Document uploaded successfully",
  "document": {
    "id": 1,
    "filename": "abc123def456.pdf",
    "original_filename": "document.pdf",
    "file_size": 1024000,
    "file_type": "pdf",
    "upload_timestamp": "2024-01-15T10:30:00"
  }
}
```

**Error Responses:**
- `400 Bad Request` - No file provided or invalid file type
- `413 Payload Too Large` - File exceeds 16MB limit
- `500 Internal Server Error` - Upload failed

### 2. List Documents

**Endpoint:** `GET /api/documents`

**Description:** List all documents with pagination

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10, max: 100)

**Request:**
```bash
curl http://127.0.0.1:5000/api/documents?page=1&per_page=10
```

**Response (200 OK):**
```json
{
  "documents": [
    {
      "id": 1,
      "filename": "abc123def456.pdf",
      "original_filename": "document.pdf",
      "file_size": 1024000,
      "file_type": "pdf",
      "upload_timestamp": "2024-01-15T10:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 1,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### 3. Retrieve Document

**Endpoint:** `GET /api/documents/<id>`

**Description:** Download a specific document by ID

**Request:**
```bash
curl http://127.0.0.1:5000/api/documents/1 -O -J
```

**Response:** Returns the document file with appropriate headers

**Error Responses:**
- `404 Not Found` - Document not found

### 4. Get Document Metadata

**Endpoint:** `GET /api/documents/<id>/metadata`

**Description:** Retrieve document metadata without downloading the file

**Request:**
```bash
curl http://127.0.0.1:5000/api/documents/1/metadata
```

**Response (200 OK):**
```json
{
  "document": {
    "id": 1,
    "filename": "abc123def456.pdf",
    "original_filename": "document.pdf",
    "file_size": 1024000,
    "file_type": "pdf",
    "upload_timestamp": "2024-01-15T10:30:00"
  }
}
```

## Configuration

The API can be configured in `app/config.py`:

- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `ALLOWED_EXTENSIONS`: Allowed file types (default: pdf, txt, docx)
- `DEFAULT_PAGE_SIZE`: Default pagination size (default: 10)
- `MAX_PAGE_SIZE`: Maximum pagination size (default: 100)

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

Run specific test file:

```bash
pytest tests/test_api.py
```

## Project Structure

```
/workspace
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # SQLAlchemy models
│   ├── routes.py            # API endpoints
│   ├── utils.py             # Helper functions
│   └── config.py            # Configuration settings
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API endpoint tests
│   └── conftest.py          # Pytest fixtures
├── uploads/                 # Directory for uploaded files
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

## Error Handling

The API implements comprehensive error handling:

- **400 Bad Request**: Invalid input (missing file, wrong file type)
- **404 Not Found**: Resource not found
- **413 Payload Too Large**: File exceeds size limit
- **500 Internal Server Error**: Server-side errors

All errors return JSON responses with an `error` field describing the issue.

## Database

The API uses SQLite for simplicity. The database file (`documents.db`) is created automatically on first run.

### Document Schema

```python
{
  "id": Integer (Primary Key),
  "filename": String (Unique, stored filename),
  "original_filename": String (Original upload name),
  "file_size": Integer (Size in bytes),
  "file_type": String (pdf/txt/docx),
  "upload_timestamp": DateTime (UTC)
}
```

## Security Features

- Secure filename generation using UUID
- File type validation
- File size limits
- SQL injection prevention via SQLAlchemy ORM
- CORS enabled for cross-origin requests

## Example Usage

### Python Example

```python
import requests

# Upload a document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://127.0.0.1:5000/api/documents', files=files)
    print(response.json())

# List documents
response = requests.get('http://127.0.0.1:5000/api/documents?page=1&per_page=10')
documents = response.json()
print(documents)

# Download a document
doc_id = 1
response = requests.get(f'http://127.0.0.1:5000/api/documents/{doc_id}')
with open('downloaded.pdf', 'wb') as f:
    f.write(response.content)
```

### cURL Examples

```bash
# Upload
curl -X POST http://127.0.0.1:5000/api/documents -F "file=@document.pdf"

# List with pagination
curl "http://127.0.0.1:5000/api/documents?page=1&per_page=5"

# Download
curl http://127.0.0.1:5000/api/documents/1 -O -J

# Get metadata
curl http://127.0.0.1:5000/api/documents/1/metadata
```

## License

MIT License

## Support

For issues or questions, please open an issue in the repository.