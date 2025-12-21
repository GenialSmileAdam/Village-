from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from auth import auth_bp
app.register_blueprint(auth_bp)







app = Flask(__name__)
csrf = CSRFProtect(app)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/sign_up")
def signup():
    return render_template("sign_up.html")

if __name__ == "__main__":
    app.run(debug=True)