"""Production WSGI entry point for Gunicorn/uWGSI"""

from myapp import create_app
from myapp import db

app = create_app("production")
with app.app_context():
    db.drop_all()
    db.create_all()
    app.logger.info("Database tables checked/created successfully")

if __name__ == '__main__':
    # This allows running: python wsgi.py (for testing)
    app.run()