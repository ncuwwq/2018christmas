# coding: utf-8

from app.user.models.user_model import User
from flask_restful import Resource, reqparse
from app.task.resources.task import getAllTasks
from app.task.models.task_model import Task as TaskModel
from app.authentication import getToken, login_required
from flask import g
from app import db
import datetime


def isLast():
    today = datetime.date.today()
    if str(today) >= '2018-12-27':
        return True
    else:
        return False


class Token(Resource):
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('user_id', type=str, required=True,
                         help=u'请输入用户名', location='json')
        req.add_argument('password', type=str, required=True,
                         help=u'请输入密码', location='json')
        args = req.parse_args()
        if (not args["user_id"]) or (not args["password"]):
            return {
                "msg": "请输入账号，密码",
                "status": 0
            }
        user = User.query.filter_by(user_id=args["user_id"]).first()
        if not user:
            return {
                "msg": u"非活动对象或账号错误",
                "status": 0
            }
        token = getToken(args['user_id'], args["password"])
        if not token:
            return {
                'msg': '密码错误',
                'status': 0
            }
        king = User.query.filter_by(username=user.king).first()
        angel = User.query.filter_by(king=user.username).first()
        return {
            'token': token,
            'kingUuid': king.uuid,
            'angelUuid': angel.uuid,
            'myUuid': user.uuid,
            'wish': user.wish,
            'status': 1
        }

    @login_required
    def get(self):
        user = User.query.filter_by(us_id=g.current_user).first()
        king = User.query.filter_by(username=user.king).first()
        angel = User.query.filter_by(king=user.username).first()
        return {
            'kingUuid': king.uuid,
            'angelUuid': angel.uuid,
            'myUuid': user.uuid,
            'wish': user.wish,
            'status': 1
        }


class Wish(Resource):

    @login_required
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('wish', type=str, required=True,
                         help=u'愿望', location='json')
        args = req.parse_args()
        if not args['wish']:
            return {
                "msg": "缺少参数",
                "status": 0
            }
        user = User.query.filter_by(us_id=g.current_user).first()
        user.wish = args['wish']
        db.session.commit()
        return {
            'status': 1
        }

    @login_required
    def get(self):
        user = User.query.filter_by(us_id=g.current_user).first()
        king = User.query.filter_by(username=user.king).first()
        return {
            "data": {"king": {"wish": king.wish, "name": king.username},
                     "wish": user.wish,
                     "mytasks": getAllTasks(g.current_user),
                     "angeltasks": TaskModel.query.filter_by(us_id=g.current_user, role='angel').count()},
            "status": 1
        }


class Last(Resource):

    @login_required
    def get(self):
        if isLast():
            user = User.query.filter_by(us_id=g.current_user).first()
            angel = User.query.filter_by(king=user.username).first()
            return {
                "status": 1,
                "angel": angel.username
            }
        else:
            return {
                "status": 0,
                "msg": "时间还没到哦"
            }
