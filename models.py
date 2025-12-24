from sqlalchemy import ForeignKey,Column, Table,Boolean,DateTime,Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Association Tables

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
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    biography: Mapped[str]
    profile_picture :Mapped[str]
	
    # AUTH FIELDS
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    biography: Mapped[str] = mapped_column(default="")
    profile_picture: Mapped[str] = mapped_column(default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    hobbies: Mapped[List["Hobby"]] = relationship(
        secondary=user_hobbies, back_populates="users", lazy="dynamic"
    )

    villages: Mapped[List["Village"]] = relationship(
        secondary=user_villages, back_populates="users", lazy="dynamic"
    )

    location_id: Mapped[int] = mapped_column(ForeignKey("location_table.id"))
    location: Mapped["Location"] = relationship(back_populates="users")

    otps: Mapped[List["OTPToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

# OTP / TOKEN MODEL


class OTPToken(db.Model):
    __tablename__ = "otp_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="otps")

    otp_hash: Mapped[str] = mapped_column(nullable=False)

    purpose: Mapped[str] = mapped_column(
        String(30), nullable=False
        # VERIFY_EMAIL | RESET_PASSWORD
    )

    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    used: Mapped[bool] = mapped_column(Boolean, default=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<OTPToken user_id={self.user_id} purpose={self.purpose}>"

# OTHER DOMAIN MODELS

class Hobby(db.Model):
    __tablename__ = "hobby_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[str]
	#Relationships
    users: Mapped[List["User"]] = relationship(
        secondary=user_hobbies, back_populates="hobbies", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Hobby {self.name}>"


class Location(db.Model):
    __tablename__ = "location_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
#Relationships
    users: Mapped[List["User"]] = relationship(
        back_populates="location", lazy="dynamic"
    )

    villages: Mapped[List["Village"]] = relationship(
        back_populates="location", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Location {self.name}>"


class Village(db.Model):
    __tablename__ = "village_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


#     Relationships
#     users: Mapped[List["User"]] = relationship(back_populates="location")

    users: Mapped[List["User"]] = relationship(
        secondary=user_villages, back_populates="villages", lazy="dynamic"
    )

    location_id: Mapped[int] = mapped_column(ForeignKey("location_table.id"))
    location: Mapped["Location"] = relationship(back_populates="villages")

    def __repr__(self):
        return f"<Location {self.name}>"
