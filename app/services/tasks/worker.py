from celery import Celery


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Moscow'
    broker_url = "redis://redis:6379/0"
    result_backend = "redis://redis:6379/0"


def celery_application() -> Celery:
    celery_app = Celery("worker",
                        broker="redis://redis:6379/0",
                        include=["app.services.tasks.tasks"])
    celery_app.config_from_object(CeleryConfig)
    return celery_app


celery_app = celery_application()
