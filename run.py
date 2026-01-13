"""Development Server entry point"""


from myapp import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)


# how to use app, run these lines of code in your terminal or git bash

# Create virtual environment (recommended)
# python -m venv venv

# Activate it:
# Windows:
#  venv\Scripts\activate

# Mac/Linux:
# source venv/bin/activate

# You should see (venv) in terminal prompt

# Make sure venv is activated, then:
# pip install -r requirements.txt

# Create a .env file in project root
# (You should use the .env.example template to create yours)



# Initialize database
# flask init-db

# Method 1: Using run.py (if you have it)
# python run.py

# Method 2: Using Flask CLI
# flask run

# The app will be at: http://localhost:5000
