from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_feedback_to_admin(author, title, text, score, reply):
    send_mail(
        f'Feedback from {author}',
        f'''Reply user: {reply}, Evaluation: {score}, Title: "{title}"
        {text}''',
        'user@example.com',
        ['admin@example.com'],
        fail_silently=False,
    )


@shared_task
def notification_for_admin(notif):
    send_mail(
        f'New {notif} on the site!',
        'Check your admin page',
        'from@example.com',
        ['admin@example.com'],
        fail_silently=False,
    )


@shared_task
def notification_for_author(post_pk):
    send_mail(
        "Hi, it's MyBlog",
        "New comment was published!",
        'from@example.com',
        ['admin@example.com'],
        fail_silently=False,
        html_message=render_to_string('blog/email_for_user.html', {'post_pk': post_pk})
    )
