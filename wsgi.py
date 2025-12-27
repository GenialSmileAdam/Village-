"""Production WSGI entry point for Gunicorn/uWGSI"""

from myapp import create_app

app = create_app("production")

if __name__ == '__main__':
    # This allows running: python wsgi.py (for testing)
    app.run()