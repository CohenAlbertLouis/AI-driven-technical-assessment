# Project Summary
The Document Management REST API is a Flask-based application designed to facilitate the upload, storage, listing, and retrieval of documents in various formats (PDF, TXT, DOCX). It aims to provide a comprehensive solution for managing document metadata, ensuring proper error handling, and offering a user-friendly interface for document management tasks.

# Project Module Description
The project consists of several functional modules:
- **Document Upload**: Allows users to upload documents while validating file types and sizes.
- **Document Listing**: Provides paginated access to all uploaded documents.
- **Document Retrieval**: Enables users to download documents by their unique IDs.
- **Metadata Storage**: Stores essential information about each document, including filename, size, type, and upload timestamp.
- **Error Handling**: Manages various errors gracefully, returning appropriate responses.

# Directory Tree
```
/workspace
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── config.py            # Configuration settings
│   ├── models.py            # SQLAlchemy models
│   ├── routes.py            # API endpoints
│   └── utils.py             # Helper functions
├── tests/
│   ├── __init__.py          # Tests package
│   ├── conftest.py          # Pytest fixtures
│   └── test_api.py          # API endpoint tests
├── uploads/                 # Directory for uploaded files
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # API documentation
```

# File Description Inventory
- **app/__init__.py**: Initializes the Flask application and sets up the database.
- **app/config.py**: Contains configuration settings for the application.
- **app/models.py**: Defines the database models used in the application.
- **app/routes.py**: Contains the API endpoints for document management.
- **app/utils.py**: Includes utility functions for file handling and validation.
- **tests/__init__.py**: Marks the tests directory as a package.
- **tests/conftest.py**: Provides fixtures for testing, including app and client setup.
- **tests/test_api.py**: Contains unit tests for the API endpoints.
- **uploads/**: Directory where uploaded documents are stored.
- **requirements.txt**: Lists the dependencies required for the project.
- **run.py**: The entry point for running the application.
- **README.md**: Documentation for the API, including usage instructions and examples.

# Technology Stack
- **Python 3.8+**
- **Flask 3.0.0**
- **Flask-SQLAlchemy 3.1.1**
- **Flask-CORS 4.0.0**
- **python-docx 1.1.0**
- **PyPDF2 3.0.1**
- **pytest 8.0.0**

# Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python run.py
   ```
