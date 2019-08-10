# coding: utf-8

from flask_restful import Resource, reqparse
from app.msg.models.msg_model import Msg as MsgModel
from app.authentication import login_required
from app.user.models.user_model import User as UserModel
from app import db
from flask import g
from sqlalchemy import or_
import datetime


def to_dict(msg, day):
    off_msg = {
        "message": msg.message,
        "time": msg.today == day and msg.time or msg.today == day - 1 and "昨天" + msg.time or "前天" + msg.time,
        "sender": msg.sender,
        "toUser": msg.toUser,
        'id': msg.uuid
    }
    return off_msg


class Msg(Resource):

    @login_required
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('msg', type=dict, required=True, location='json')
        args = req.parse_args()
        get_msg = args['msg']
        msg = MsgModel(message=get_msg['message'], time=get_msg['time'], uuid=get_msg['id'],
                       sender=get_msg['sender'], toUser=get_msg['toUser'], today=datetime.date.today().day)
        db.session.add(msg)
        db.session.commit()
        return {
            "status": 1
        }

    @login_required
    def get(self):
        day = datetime.date.today().day
        user = UserModel.query.filter_by(us_id=g.current_user).first()
        msgs = MsgModel.query.filter(or_(MsgModel.sender == user.uuid, MsgModel.toUser == user.uuid),
                                     MsgModel.today.between(day - 2, day)).all()
        if not msgs:
            return {
                "status": 0,
            }
        off_msg = []
        for m in msgs:
            off_msg.append(to_dict(m, day))
        return {
            "status": 1,
            "off_msg": off_msg,
        }


class Read(Resource):

    @login_required
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('toUser', type=str, required=True, location='json')
        args = req.parse_args()
        toUser = UserModel.query.filter_by(uuid=args['toUser']).first()
        user = UserModel.query.filter_by(us_id=g.current_user).first()
        if user.king == toUser.username:
            if toUser.angel_unread:
                return {
                    "status": 1
                }
            toUser.angel_unread = True
            db.session.commit()
        else:
            if toUser.king_unread:
                return {
                    "status": 1
                }
            toUser.king_unread = True
            db.session.commit()
        return {
            "status": 1
        }

    @login_required
    def get(self):
        user = UserModel.query.filter_by(us_id=g.current_user).first()
        if user.king_unread:
            user.king_unread = False
            db.session.commit()
        if user.angel_unread:
            user.angel_unread = False
            db.session.commit()
        return {
            "status": 1
        }
