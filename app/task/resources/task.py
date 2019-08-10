# coding: utf-8

from flask_restful import Resource, reqparse
from app.user.models.user_model import User as UserModel
from app.task.models.task_model import Task as TaskModel
from app.authentication import login_required
from app import db
from flask import g
import datetime
import time
from app.config import Config


def getAllTasks(us_id):
    user = UserModel.query.filter_by(us_id=us_id).first()
    king = UserModel.query.filter_by(username=user.king).first()
    tasks = TaskModel.query.filter_by(us_id=king.us_id, role='angel').count()
    return tasks


def getTask(us_id, role):
    today = datetime.date.today()
    task = TaskModel.query.filter_by(us_id=us_id, role=role, datetime=today).first()
    if not task:
        return False
    return True


class Task(Resource):

    @login_required
    def post(self):
        req = reqparse.RequestParser()
        req.add_argument('role', type=str, required=True,
                         help=u'身份', location='json')
        args = req.parse_args()
        if getTask(g.current_user, args['role']):
            return {
                "msg": "今日任务已完成",
                "status": 0
            }
        if args['role'] == 'angel':
            user = UserModel.query.filter_by(us_id=g.current_user).first()
            angel = UserModel.query.filter_by(king=user.username).first()
            if not getTask(angel.us_id, 'king'):
                return {
                    "msg": "你的天使还没有请求苹果呢",
                    "status": 0
                }
        task = TaskModel(us_id=g.current_user, role=args["role"], datetime=datetime.date.today())
        db.session.add(task)
        db.session.commit()
        return {
            "msg": "已提交",
            "status": 1,
            "mytasks": getAllTasks(g.current_user),
            "angeltasks": TaskModel.query.filter_by(us_id=g.current_user, role='angel').count()
        }

    @login_required
    def get(self):
        user = UserModel.query.filter_by(us_id=g.current_user).first()
        kingWork = getTask(g.current_user, 'king')
        angelWork = getTask(g.current_user, 'angel')
        return {
            "kingWork": kingWork,
            "angelWork": angelWork,
            "status": 1,
            "king_unread": user.king_unread,
            "angel_unread": user.angel_unread
        }


class Plan(Resource):

    @login_required
    def get(self):
        today = datetime.date.today()
        plan = Config.ALL_PLAN.get(str(today))
        if plan:
            return {
                "status": 1,
                "plan": plan
            }
        else:
            return {
                "status": 0,
                "msg": "今日没有任务"
            }
