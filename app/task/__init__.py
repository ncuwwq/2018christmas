# coding: utf-8
from flask import Blueprint
from flask_restful import Api
from app.task.resources.task import Task
from app.task.resources.task import Plan

task = Blueprint('task', __name__)
task_api = Api(task)

task_api.add_resource(Task, '/task')
task_api.add_resource(Plan, '/plan')


