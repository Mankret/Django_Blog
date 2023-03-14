import celery
from celery import shared_task

from django.core.mail import send_mail


@shared_task()
def send_system_message(subj, message, email):
    send_mail(
        f'{subj}',
        f'{message}',
        f'{email}',
        ['admin@admin.com'],
    )
    return 'system notification'


@shared_task()
def send_system_message_for_author(email, url):
    send_mail(
        'New comment',
        f'New comment added, check your post: {url}',
        'system@admin.com',
        [email],
    )
    return 'system notification'


#
# class SendTask(celery.Task):
#
#     @shared_task()
#     def send_system_message(self):
#         send_mail(
#             'New comment',
#             'New comment added, check admin page',
#             'system@admin.com',
#             ['admin@admin.com'],
#         )
#         return 'system notification'