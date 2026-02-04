# API Documentation
## Document Management REST API

**Base URL:** `http://127.0.0.1:5000/api`  
**Version:** 1.0  
**Protocol:** HTTP/HTTPS  
**Format:** JSON

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Error Handling](#error-handling)
4. [Rate Limiting](#rate-limiting)
5. [Endpoints](#endpoints)
   - [Upload Document](#1-upload-document)
   - [List Documents](#2-list-documents)
   - [Retrieve Document](#3-retrieve-document)
   - [Get Document Metadata](#4-get-document-metadata)
6. [Data Models](#data-models)
7. [Status Codes](#status-codes)
8. [Examples](#examples)
9. [SDKs and Libraries](#sdks-and-libraries)

---

## Overview

The Document Management REST API provides a simple and secure way to upload, store, retrieve, and manage documents. The API supports PDF, TXT, and DOCX file formats with a maximum file size of 16MB.

### Key Features

- ✅ Document upload with validation
- ✅ Metadata storage (filename, size, type, timestamp)
- ✅ Paginated document listing
- ✅ Individual document retrieval
- ✅ Comprehensive error handling
- ✅ Security measures (file validation, SQL injection prevention, path traversal protection)

### Supported File Types

- **PDF** (.pdf)
- **Text** (.txt)
- **Word Document** (.docx)

### Limitations

- Maximum file size: 16MB
- Maximum pagination size: 100 items per page
- Supported file types: PDF, TXT, DOCX only

---

## Authentication

**Current Version:** No authentication required

**Future Versions:** Will support JWT token-based authentication

```http
Authorization: Bearer <token>
```

---

## Error Handling

All errors return a JSON response with an `error` field containing a human-readable message.

### Error Response Format

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Scenarios

| Error | Status Code | Description |
|-------|-------------|-------------|
| No file provided | 400 | Request missing 'file' field |
| Invalid file type | 400 | File extension not in allowed list |
| File too large | 413 | File exceeds 16MB limit |
| Document not found | 404 | Document ID doesn't exist |
| Method not allowed | 405 | Wrong HTTP method used |
| Internal server error | 500 | Unexpected server error |

---

## Rate Limiting

**Current Version:** No rate limiting

**Future Versions:** Will implement rate limiting per IP address

---

## Endpoints

### 1. Upload Document

Upload a new document to the system.

#### Request

```http
POST /api/documents
Content-Type: multipart/form-data
```

**Form Data:**
- `file` (required): The document file to upload

#### Response

**Success (201 Created):**

```json
{
  "message": "Document uploaded successfully",
  "document": {
    "id": 1,
    "filename": "a1b2c3d4e5f6789...abc.pdf",
    "original_filename": "report.pdf",
    "file_size": 1024000,
    "file_type": "pdf",
    "upload_timestamp": "2026-02-04T10:30:00.000000"
  }
}
```

**Error Responses:**

```json
// 400 Bad Request - No file provided
{
  "error": "No file provided"
}

// 400 Bad Request - Invalid file type
{
  "error": "Invalid file type. Allowed types: PDF, TXT, DOCX"
}

// 413 Payload Too Large
{
  "error": "File too large"
}

// 500 Internal Server Error
{
  "error": "Upload failed: [error details]"
}
```

#### cURL Example

```bash
curl -X POST http://127.0.0.1:5000/api/documents \
  -F "file=@/path/to/document.pdf"
```

#### Python Example

```python
import requests

url = "http://127.0.0.1:5000/api/documents"
files = {'file': open('document.pdf', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

#### JavaScript Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:5000/api/documents', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 2. List Documents

Retrieve a paginated list of all documents.

#### Request

```http
GET /api/documents?page={page}&per_page={per_page}
```

**Query Parameters:**

| Parameter | Type | Required | Default | Min | Max | Description |
|-----------|------|----------|---------|-----|-----|-------------|
| page | integer | No | 1 | 1 | ∞ | Page number |
| per_page | integer | No | 10 | 1 | 100 | Items per page |

#### Response

**Success (200 OK):**

```json
{
  "documents": [
    {
      "id": 3,
      "filename": "xyz789...def.txt",
      "original_filename": "notes.txt",
      "file_size": 2048,
      "file_type": "txt",
      "upload_timestamp": "2026-02-04T12:00:00.000000"
    },
    {
      "id": 2,
      "filename": "abc123...ghi.docx",
      "original_filename": "document.docx",
      "file_size": 512000,
      "file_type": "docx",
      "upload_timestamp": "2026-02-04T11:30:00.000000"
    },
    {
      "id": 1,
      "filename": "def456...jkl.pdf",
      "original_filename": "report.pdf",
      "file_size": 1024000,
      "file_type": "pdf",
      "upload_timestamp": "2026-02-04T10:30:00.000000"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 3,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

**Error Response:**

```json
// 500 Internal Server Error
{
  "error": "Failed to retrieve documents: [error details]"
}
```

#### cURL Example

```bash
# Get first page with default size (10 items)
curl http://127.0.0.1:5000/api/documents

# Get second page with 20 items per page
curl "http://127.0.0.1:5000/api/documents?page=2&per_page=20"
```

#### Python Example

```python
import requests

url = "http://127.0.0.1:5000/api/documents"
params = {'page': 1, 'per_page': 10}
response = requests.get(url, params=params)
data = response.json()

print(f"Total documents: {data['pagination']['total_items']}")
for doc in data['documents']:
    print(f"- {doc['original_filename']} ({doc['file_size']} bytes)")
```

#### JavaScript Example

```javascript
fetch('http://127.0.0.1:5000/api/documents?page=1&per_page=10')
  .then(response => response.json())
  .then(data => {
    console.log(`Total: ${data.pagination.total_items}`);
    data.documents.forEach(doc => {
      console.log(`${doc.original_filename} - ${doc.file_type}`);
    });
  });
```

---

### 3. Retrieve Document

Download a specific document by its ID.

#### Request

```http
GET /api/documents/{id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Document ID |

#### Response

**Success (200 OK):**

Returns the document file as a binary stream with appropriate headers:

```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="original_filename.pdf"
```

**Error Responses:**

```json
// 404 Not Found - Document doesn't exist
{
  "error": "Document not found"
}

// 404 Not Found - File missing from storage
{
  "error": "Document file not found"
}

// 500 Internal Server Error
{
  "error": "Failed to retrieve document: [error details]"
}
```

#### cURL Example

```bash
# Download document with ID 1
curl http://127.0.0.1:5000/api/documents/1 -O -J

# The -O flag saves the file
# The -J flag uses the server-provided filename
```

#### Python Example

```python
import requests

url = "http://127.0.0.1:5000/api/documents/1"
response = requests.get(url)

if response.status_code == 200:
    # Get filename from Content-Disposition header
    filename = response.headers.get('Content-Disposition').split('filename=')[1].strip('"')
    
    # Save file
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {filename}")
else:
    print(f"Error: {response.json()['error']}")
```

#### JavaScript Example

```javascript
fetch('http://127.0.0.1:5000/api/documents/1')
  .then(response => {
    if (response.ok) {
      return response.blob();
    }
    throw new Error('Download failed');
  })
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'document.pdf';
    a.click();
  });
```

---

### 4. Get Document Metadata

Retrieve document metadata without downloading the file.

#### Request

```http
GET /api/documents/{id}/metadata
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Document ID |

#### Response

**Success (200 OK):**

```json
{
  "document": {
    "id": 1,
    "filename": "a1b2c3d4e5f6789...abc.pdf",
    "original_filename": "report.pdf",
    "file_size": 1024000,
    "file_type": "pdf",
    "upload_timestamp": "2026-02-04T10:30:00.000000"
  }
}
```

**Error Responses:**

```json
// 404 Not Found
{
  "error": "Document not found"
}

// 500 Internal Server Error
{
  "error": "Failed to retrieve metadata: [error details]"
}
```

#### cURL Example

```bash
curl http://127.0.0.1:5000/api/documents/1/metadata
```

#### Python Example

```python
import requests

url = "http://127.0.0.1:5000/api/documents/1/metadata"
response = requests.get(url)
doc = response.json()['document']

print(f"Filename: {doc['original_filename']}")
print(f"Size: {doc['file_size']} bytes")
print(f"Type: {doc['file_type']}")
print(f"Uploaded: {doc['upload_timestamp']}")
```

#### JavaScript Example

```javascript
fetch('http://127.0.0.1:5000/api/documents/1/metadata')
  .then(response => response.json())
  .then(data => {
    const doc = data.document;
    console.log(`${doc.original_filename} (${doc.file_size} bytes)`);
  });
```

---

## Data Models

### Document Object

Represents a document in the system.

```json
{
  "id": 1,
  "filename": "a1b2c3d4e5f6789abcdef0123456789.pdf",
  "original_filename": "report.pdf",
  "file_size": 1024000,
  "file_type": "pdf",
  "upload_timestamp": "2026-02-04T10:30:00.000000"
}
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique document identifier |
| filename | string | UUID-based stored filename (internal use) |
| original_filename | string | User-provided filename (sanitized) |
| file_size | integer | File size in bytes |
| file_type | string | File extension (pdf, txt, docx) |
| upload_timestamp | string | ISO 8601 formatted upload date/time (UTC) |

### Pagination Object

Provides pagination metadata for list responses.

```json
{
  "page": 1,
  "per_page": 10,
  "total_items": 42,
  "total_pages": 5,
  "has_next": true,
  "has_prev": false
}
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| page | integer | Current page number |
| per_page | integer | Items per page |
| total_items | integer | Total number of documents |
| total_pages | integer | Total number of pages |
| has_next | boolean | Whether next page exists |
| has_prev | boolean | Whether previous page exists |

---

## Status Codes

The API uses standard HTTP status codes:

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST request (document uploaded) |
| 400 | Bad Request | Invalid input (missing file, wrong type, etc.) |
| 404 | Not Found | Resource not found (document doesn't exist) |
| 405 | Method Not Allowed | Wrong HTTP method used |
| 413 | Payload Too Large | File size exceeds 16MB limit |
| 500 | Internal Server Error | Unexpected server error |

---

## Examples

### Complete Workflow Example (Python)

```python
import requests

BASE_URL = "http://127.0.0.1:5000/api"

# 1. Upload a document
print("1. Uploading document...")
with open('report.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/documents", files=files)
    upload_result = response.json()
    doc_id = upload_result['document']['id']
    print(f"   Uploaded! Document ID: {doc_id}")

# 2. List all documents
print("\n2. Listing documents...")
response = requests.get(f"{BASE_URL}/documents?page=1&per_page=10")
data = response.json()
print(f"   Total documents: {data['pagination']['total_items']}")
for doc in data['documents']:
    print(f"   - {doc['original_filename']} ({doc['file_size']} bytes)")

# 3. Get document metadata
print(f"\n3. Getting metadata for document {doc_id}...")
response = requests.get(f"{BASE_URL}/documents/{doc_id}/metadata")
metadata = response.json()['document']
print(f"   Filename: {metadata['original_filename']}")
print(f"   Size: {metadata['file_size']} bytes")
print(f"   Type: {metadata['file_type']}")
print(f"   Uploaded: {metadata['upload_timestamp']}")

# 4. Download the document
print(f"\n4. Downloading document {doc_id}...")
response = requests.get(f"{BASE_URL}/documents/{doc_id}")
if response.status_code == 200:
    filename = f"downloaded_{metadata['original_filename']}"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"   Downloaded to: {filename}")
```

### Error Handling Example (Python)

```python
import requests

def upload_document(filepath):
    """Upload a document with proper error handling."""
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                "http://127.0.0.1:5000/api/documents",
                files=files
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"Success! Document ID: {data['document']['id']}")
                return data['document']
            
            elif response.status_code == 400:
                error = response.json()['error']
                print(f"Bad request: {error}")
                return None
            
            elif response.status_code == 413:
                print("Error: File too large (max 16MB)")
                return None
            
            else:
                print(f"Unexpected error: {response.status_code}")
                return None
                
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

# Usage
document = upload_document('report.pdf')
```

### Pagination Example (JavaScript)

```javascript
async function getAllDocuments() {
  const allDocuments = [];
  let page = 1;
  let hasMore = true;
  
  while (hasMore) {
    const response = await fetch(
      `http://127.0.0.1:5000/api/documents?page=${page}&per_page=20`
    );
    const data = await response.json();
    
    allDocuments.push(...data.documents);
    hasMore = data.pagination.has_next;
    page++;
  }
  
  return allDocuments;
}

// Usage
getAllDocuments().then(docs => {
  console.log(`Retrieved ${docs.length} documents`);
  docs.forEach(doc => {
    console.log(`- ${doc.original_filename}`);
  });
});
```

---

## SDKs and Libraries

### Python

**Recommended Library:** `requests`

```bash
pip install requests
```

### JavaScript/Node.js

**Browser:** Native `fetch` API  
**Node.js:** `node-fetch` or `axios`

```bash
npm install axios
```

### cURL

Available on most Unix-like systems and Windows 10+

---

## Changelog

### Version 1.0 (2026-02-04)

**Initial Release:**
- Document upload endpoint
- Document listing with pagination
- Document retrieval endpoint
- Document metadata endpoint
- Comprehensive error handling
- Security measures (file validation, SQL injection prevention)

---

## Support

For issues, questions, or feature requests:

- **Documentation:** See README.md in the project root
- **Testing:** Run `pytest tests/` to verify functionality
- **Security:** Report security issues privately

---

## License

MIT License

---

**Last Updated:** February 4, 2026  
**API Version:** 1.0  
**Documentation Version:** 1.0