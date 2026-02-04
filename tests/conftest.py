"""Pytest configuration and fixtures."""
import pytest
import os
import tempfile
import shutil
from app import create_app, db

@pytest.fixture
def app():
    """Create application for testing."""
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    # Create a temporary upload folder
    upload_folder = tempfile.mkdtemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'UPLOAD_FOLDER': upload_folder,
        'MAX_CONTENT_LENGTH': 16 * 1024 * 1024
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(upload_folder, ignore_errors=True)

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()