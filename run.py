"""Application entry point."""
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    print("=" * 50)
    print("Document Management REST API")
    print("=" * 50)
    print("API Endpoints:")
    print("  POST   /api/documents        - Upload a document")
    print("  GET    /api/documents        - List all documents (with pagination)")
    print("  GET    /api/documents/<id>   - Retrieve a specific document")
    print("=" * 50)
    print("Server running on http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)