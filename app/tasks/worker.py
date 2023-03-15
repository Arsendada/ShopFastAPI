from celery import Celery


class CeleryConfig:
    enable_utc = True
    broker_url = "redis://redis:6379"


def celery_application() -> Celery:
    celery_app = Celery("worker", backend='redis', broker="redis://redis:6379")
    celery_app.config_from_object(CeleryConfig)
    return celery_app


celery_app = celery_application()