from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="tenant", nullable=False)

    listings = db.relationship("Listing", backref="landlord", lazy=True)
    requests = db.relationship("BookingRequest", backref="tenant", lazy=True)


class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    availability_status = db.Column(db.String(20), default="available", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    landlord_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    booking_requests = db.relationship("BookingRequest", backref="listing", lazy=True)


class BookingRequest(db.Model):
    __tablename__ = "booking_requests"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
