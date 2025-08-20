#!/usr/bin/env python3
"""
WSGI entry point for Gunicorn production server
This file is required for production deployment with Gunicorn
"""

from app import app

if __name__ == "__main__":
    app.run() 