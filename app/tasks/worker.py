from celery import Celery


class CeleryConfig:
    enable_utc = True
    broker_url = "redis://guest:guest@localhost:6379/0"


def celery_application() -> Celery:
    celery_app = Celery("worker", backend='redis', broker="redis://guest:guest@localhost:6379/0")
    celery_app.config_from_object(CeleryConfig)
    return celery_app


celery_app = celery_application()