from django.dispatch import Signal, receiver

from rabbit import get_rabbit_channel
from utils import send_email


robot_created = Signal()

EMAIL_CREATED_ROBOT_SUBJECT = "Робот появился в наличии!"
EMAIL_CREATED_ROBOT_MESSAGE = (
    "Добрый день!\n"
    "Недавно вы интересовались нашим роботом "
    "модели %(model)s, версии %(version)s.\n"
    "Этот робот теперь в наличии. "
    "Если вам подходит этот вариант "
    "- пожалуйста, свяжитесь с нами."
)


@receiver(robot_created)
def send_emails_to_customers(sender, **kwargs):
    # TODO: Перенести на Celery
    robot = kwargs.get("robot")
    with get_rabbit_channel() as channel:
        for _ in range(
            channel.queue_declare(robot["serial"], passive=True).method.message_count
        ):
            method, properties, body = channel.basic_get(robot["serial"])
            email = body.decode("utf-8")
            send_email(
                to_email=email,
                subject=EMAIL_CREATED_ROBOT_SUBJECT,
                message=EMAIL_CREATED_ROBOT_MESSAGE
                % {"model": robot["model"], "version": robot["version"]},
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
