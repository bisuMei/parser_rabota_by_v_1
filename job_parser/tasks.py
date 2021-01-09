# Create your tasks here
import celery
from celery import shared_task
from celery.schedules import crontab
from job_parser import script_parser


@shared_task
def add():
    script_parser.parse_all()


