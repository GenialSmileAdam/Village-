



# app = Flask(__name__)
#     # -----------DATABASE CONFIGURATION --------------
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///village.db"
#
#
#
#
# db.init_app(app)




# with app.app_context():
#     db.create_all()

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



# if __name__ == "__main__":
#     app.run(debug=True)