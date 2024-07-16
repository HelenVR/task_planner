import os
from loguru import logger
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from django.core.mail import send_mail
import datetime

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@receiver(post_save, sender=Task)
def update_or_create_task(sender, instance, created, **kwargs):
    job_id = f"task_{instance.id}"
    if scheduler.get_job(job_id, jobstore="default"):
        scheduler.remove_job(job_id, jobstore="default")
    time_obj = datetime.datetime.strptime(instance.notification_time, "%H:%M:%S")
    start_date = datetime.datetime.now().replace(hour=time_obj.hour, minute=time_obj.minute, second=time_obj.second)
    if instance.notification_interval:
        scheduler.add_job(
            send_email_notification,
            'interval',
            id=job_id,
            minutes=2, #get_interval_in_minutes(instance.notification_interval),
            replace_existing=True,
            args=[instance.id]
        )
        logger.info(f'Notification task added: {instance.notification_interval}')


@receiver(post_delete, sender=Task)
def delete_task(sender, instance, **kwargs):
    job_id = f"task_{instance.id}"
    if scheduler.get_job(job_id, jobstore="default"):
        scheduler.remove_job(job_id, jobstore="default")


def send_email_notification(task_id):
    task = Task.objects.get(id=task_id)
    if task.email:
        message = f"Task: {task.name}\nDescription: {task.task}\nDeadline: {task.deadline}"
        subject = 'Notification'
        from_email = 't36176985@gmail.com'
        recipient_list = [task.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            logger.info(f'Email notification sent')
        except Exception as e:
            logger.error(f'Failed to send email: {e.__class__.__name__}, {e}')


def get_interval_in_minutes(interval):
    if interval == 'hour':
        return 60
    elif interval == 'day':
        return 1440
    return 1


scheduler.start()