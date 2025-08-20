#!/usr/bin/env python3
"""
WSGI entry point for Gunicorn production server
This file is ONLY used in production with Gunicorn
"""

# Import the Flask app instance
from app import app

# This is what Gunicorn will use
app = app

if __name__ == "__main__":
    # This won't run in production, only if someone manually runs wsgi.py
    app.run(debug=False, host='0.0.0.0', port=5000) 