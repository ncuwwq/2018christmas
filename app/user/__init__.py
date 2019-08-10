# coding: utf-8
from flask import Blueprint
from flask_restful import Api

from app.user.resources.user import Token, Wish, Last

user = Blueprint('user', __name__)
user_api = Api(user)

user_api.add_resource(Token, '/token')
user_api.add_resource(Wish, '/wish')
user_api.add_resource(Last, '/last')
