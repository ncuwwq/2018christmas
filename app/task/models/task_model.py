# coding: utf-8
from app import db


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    us_id = db.Column(db.Integer, index=True)
    role = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
