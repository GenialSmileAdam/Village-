from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from models import db, User, Hobby



app = Flask(__name__)
csrf = CSRFProtect(app)
    # -----------DATABASE CONFIGURATION --------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///village.db"





db.init_app(app)




# with app.app_context():
#     db.create_all()

# inserting data for test cases
# with app.app_context():
#     for i in range(1,10):
#         user = User(username= f"user{i}",
#                     email= f"user{i}@gmail.com",
#                     biography= "generic ass bio.",
#                     profile_picture = "https://i.pinimg.com/736x/fa/d5/e7/fad5e79954583ad50ccb3f16ee64f66d.jpg")
#         db.session.add(user)
#     for i in range(1, 3):
#         hobby = Hobby(name=f"hobby{i}")
#         db.session.add(hobby)
#     db.session.commit()
#
# with app.app_context():
#     hobby = Hobby(name="Chess")
#     db.session.add(hobby)
#     db.session.commit()


# with app.app_context():
#     user =db.session.scalar(select(User).where(User.id == 1))
#     hobby=db.session.scalar(select(Hobby).where(Hobby.id == 1))
#
# #     associate
#     user.hobbies.append(hobby)
#     db.session.commit()


# creating associations
# with app.app_context():
#     users = db.session.scalars(select(User).order_by(User.id)).all()
#     hobby1 = db.session.scalar(select(Hobby).where(Hobby.name == "hobby1"))
#     hobby2 = db.session.scalar(select(Hobby).where(Hobby.name == "hobby2"))
#
#     for user in users[:5]:
#         user.hobbies.append(hobby1)
#     for user in users[5:]:
#         user.hobbies.append(hobby2)
#     db.session.commit()


# accessing Users from a hobby
# with app.app_context():
#     hobby  = db.session.scalar(select(Hobby).where(Hobby.name == "hobby1"))
#     users_hobby1 = hobby.users
#     for user in users_hobby1:
#         print(user)

# Accessing Hobbies from a User
# with app.app_context():
#     user  = db.session.scalar(select(User).where(User.id == 1))
#     user1_hobbies = user.hobbies
#     for hobby in user1_hobbies:
#         print(hobby)


# Removing Hobby from a User
# with app.app_context():
#     user  = db.session.scalar(select(User).where(User.id == 1))
    # hobby  = db.session.scalar(select(Hobby).where(Hobby.name == "hobby1"))
    # user.hobbies.remove(hobby)
    # db.session.commit()
    # for hobby in user.hobbies:
    #     print(hobby)

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