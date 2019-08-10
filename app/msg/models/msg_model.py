# coding: utf-8
from app import db


class Msg(db.Model):
    __tablename__ = 'msg'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    sender = db.Column(db.String, nullable=False, index=True)
    time = db.Column(db.String, nullable=False)
    toUser = db.Column(db.String, nullable=False, index=True)
    uuid = db.Column(db.String)
    today = db.Column(db.Integer, index=True)
