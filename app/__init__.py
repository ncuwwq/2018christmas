# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import SqlConfig

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(SqlConfig)
    SqlConfig.init_app(app)

    db.init_app(app)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/user')

    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/api/task')

    from .msg import msg as msg_blueprint
    app.register_blueprint(msg_blueprint, url_prefix='/api/msg')

    return app
