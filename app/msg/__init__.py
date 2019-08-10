# coding: utf-8
from flask import Blueprint
from flask_restful import Api
from app.msg.resources.msg import Msg, Read

msg = Blueprint('msg', __name__)
msg_api = Api(msg)

msg_api.add_resource(Msg, '/msg')
msg_api.add_resource(Read, '/read')
