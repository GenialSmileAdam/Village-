"""Development Server entry point"""

import os

from myapp import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

"""
# how to use app, run these lines of code in your terminal or git bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy flask-login flask-wtf flask-migrate python-dotenv

# Save requirements
pip freeze > requirements.txt
"""