# coding: utf-8
from app.user.models.user_model import User
from app import db, config
from flask import g, request, abort
from functools import wraps
import requests
import jwt
import json


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token == '':
            return {
                "status": 0,
                "msg": "token为空"
            }
        user = encode_token(token)
        if not user:
            return {
                "status": 0,
                "msg": "无效的token"
            }
        g.current_user = user
        return func(*args, **kwargs)

    return inner


def encode_token(token):
    key = config.Config.SECRET_KEY
    try:
        info = jwt.decode(token, key, options={'require_exp': True})
        user = User.query.filter_by(us_id=info["user_id"]).first()
        db.session.commit()
        if not user:
            return {
                "msg": u"非活动用户对象",
                "status": 0
            }
        return info['user_id']
    except Exception as e:
        return False


def getToken(user_id, password):
    url = "http://us.ncuos.com/api/user/login"
    headers = {'Content-Type': 'application/json'}
    data = {"username": user_id, "password": password}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    try:
        token = response.headers['Authorization']
        info = response.json()
        user = User.query.filter_by(user_id=user_id).first()
        user.photo = info['photo']
        db.session.commit()
        return token
    except Exception as e:
        return None
