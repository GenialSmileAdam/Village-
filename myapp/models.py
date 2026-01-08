from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from .extensions import db, Base




user_hobbies = Table(
    "user_hobbies_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("hobby_id", ForeignKey("hobby_table.id"), primary_key=True)
)

user_villages = Table(
    "user_village_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("village_id", ForeignKey("village_table.id"), primary_key=True)
)

hobby_villages = Table(
    "hobby_village_association_table",
    Base.metadata,
    Column("hobby_id", ForeignKey("hobby_table.id"), primary_key=True),
    Column("village_id", ForeignKey("village_table.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name:Mapped[int]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]
    biography: Mapped[Optional[str]]
    profile_picture :Mapped[Optional[str]]

    # Relationships
    hobbies :Mapped[List['Hobby']] = relationship(secondary=user_hobbies,
                                                  back_populates="users", lazy="dynamic")

    villages: Mapped[List['Village']] = relationship(secondary=user_villages,
                                                     back_populates="users", lazy="dynamic")

    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("location_table.id"))
    location: Mapped[Optional["Location"]] = relationship(back_populates="users")

    def __repr__(self):
        return f"User {self.username}"

class Hobby(db.Model):
    __tablename__ = "hobby_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category:Mapped[str]

    # Relationships
    users :Mapped[List["User"]] = relationship(secondary=user_hobbies,
                                               back_populates="hobbies", lazy="dynamic")

    villages: Mapped[List['Village']] = relationship(secondary=hobby_villages,
                                                     back_populates="hobbies", lazy="dynamic")

    def __repr__(self):
        return f"Hobby {self.name}"

class Location(db.Model):
    __tablename__ = "location_table"

    id :Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

#     Relationships
    users: Mapped[List["User"]] = relationship(back_populates="location", lazy="dynamic")

    villages: Mapped[List["Village"]] = relationship(back_populates="location", lazy="dynamic")


    def __repr__(self):
        return f"Location {self.name}"


class Village(db.Model):
    __tablename__ = "village_table"

    id :Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

#     Relationships
    users: Mapped[List['User']] = relationship(secondary=user_villages,
                                               back_populates="villages", lazy="dynamic")

    hobbies: Mapped[List['Hobby']] = relationship(secondary=hobby_villages,
                                                  back_populates="villages", lazy="dynamic")

    location_id: Mapped[int] = mapped_column(ForeignKey("location_table.id"))
    location: Mapped["Location"] = relationship(back_populates="villages")

    def __repr__(self):
        return f"Village {self.name}"





# def add_test_data():
#
# # inserting data for test cases
#     with app.app_context():
#         for i in range(1,20):
#             user = User(username= f"user{i}",
#                         email= f"user{i}@gmail.com",
#                         biography= "generic ass bio.",
#                         profile_picture = "https://i.pinimg.com/736x/fa/d5/e7/fad5e79954583ad50ccb3f16ee64f66d.jpg")
#             db.session.add(user)
#
#         for i in range(1, 3):
#             hobby = Hobby(name=f"hobby{i}")
#             db.session.add(hobby)
#         db.session.commit()












