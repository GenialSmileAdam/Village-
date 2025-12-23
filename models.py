from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)






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



class User(db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    biography: Mapped[str]
    profile_picture :Mapped[str]

    # Relationships
    hobbies :Mapped[List['Hobby']] = relationship(secondary=user_hobbies, back_populates="users", lazy="dynamic")

    villages: Mapped[List['Village']] = relationship(secondary=user_hobbies, back_populates="users", lazy="dynamic")

    location_id: Mapped[int] = mapped_column(ForeignKey("location_table.id"))
    location: Mapped["Location"] = relationship(back_populates="users")

    def __repr__(self):
        return f"User {self.username}"

class Hobby(db.Model):
    __tablename__ = "hobby_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category:Mapped[str]

    # Relationships
    users :Mapped[List["User"]] = relationship(secondary=user_hobbies, back_populates="hobbies", lazy="dynamic")

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
#     users: Mapped[List["User"]] = relationship(back_populates="location")
    users: Mapped[List['User']] = relationship(secondary=user_villages, back_populates="villages", lazy="dynamic")

    location_id: Mapped[int] = mapped_column(ForeignKey("location_table.id"))
    location: Mapped["Location"] = relationship(back_populates="villages")

    def __repr__(self):
        return f"Location {self.name}"


















