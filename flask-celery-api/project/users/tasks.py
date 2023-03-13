import logging

from celery.signals import after_setup_logger
import random

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from project.celery_utils import custom_celery_task
from project.users.service import user_service

logger = get_task_logger(__name__)


@shared_task()
def sample_task():
    user_service.api_call()


@custom_celery_task(max_retries=3)
def task_process_notification():
    user_service.api_call()


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.users.events import update_celery_task_status
    update_celery_task_status(task_id)


@shared_task(name='task_schedule_work')
def task_schedule_work():
    logger.info('task_schedule_work run')


@shared_task(name='default:dynamic_example_one')
def dynamic_example_one():
    logger.info('Example One')


@shared_task(name='low_priority:dynamic_example_two')
def dynamic_example_two():
    logger.info('Example Two')


@shared_task(name='high_priority:dynamic_example_three')
def dynamic_example_three():
    logger.info('Example Three')


@shared_task()
def task_send_welcome_email(user_pk):
    from project.users.models import User
    user = User.query.get(user_pk)
    logger.info(f'send email to {user.email} {user.id}')


@shared_task()
def task_test_logger():
    logger.info('test')


@after_setup_logger.connect()
def on_after_setup_logger(logger, **kwargs):
    formatter = logger.handlers[0].formatter
    file_handler = logging.FileHandler('celery.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


