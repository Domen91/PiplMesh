from celery import task

from horoscope import update_all_horoscope

@task.task
def update_horoscope():
    update_all_horoscope()