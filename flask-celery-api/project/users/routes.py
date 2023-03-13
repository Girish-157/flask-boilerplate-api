import random
import logging
from string import ascii_lowercase

import requests
from celery.result import AsyncResult
from flask import Blueprint, render_template, flash, abort, request, Response, jsonify, current_app

from project.users.service import user_service
from . import users_blueprint
from project import csrf, db
from project.users.models import User
from project.users.tasks import (
    sample_task,
    task_process_notification,
    task_send_welcome_email,
)



@users_blueprint.route('/task_status/', methods=('GET', 'POST'))
def task_status():
    task_id = request.args.get('task_id')

    if task_id:
        task = AsyncResult(task_id)
        state = task.state

        if state == 'FAILURE':
            error = str(task.result)
            response = {
                'state': state,
                'error': error,
            }
        else:
            response = {
                'state': state,
            }
        return jsonify(response)


@users_blueprint.route('/test', methods=('POST', ))
@csrf.exempt
def webhook_test():
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post('https://httpbin.org/delay/5')
    return 'pong'


@users_blueprint.route('/test_async', methods=('POST', ))
@csrf.exempt
def webhook_test_async():
    task = task_process_notification.delay()
    current_app.logger.info(task.id)
    return 'pong'


@users_blueprint.route('/create_user', methods=('POST'))
def create_user():
    try:
        username = user_service.random_username()
        user = User(
            username=f'{username}',
            email=f'{username}@test.com',
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise

    current_app.logger.info(f'user {user.id} {user.username} is persistent now')
    task_send_welcome_email.delay(user.id)
    return 'done'

