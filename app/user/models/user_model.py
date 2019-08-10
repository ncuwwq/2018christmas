# coding: utf-8
from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    us_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.String, index=True)
    username = db.Column(db.String, index=True)
    uuid = db.Column(db.INT, index=True)
    king = db.Column(db.String, index=True)
    department = db.Column(db.String)
    wish = db.Column(db.TEXT)
    angel_unread = db.Column(db.Boolean)
    king_unread = db.Column(db.Boolean)
