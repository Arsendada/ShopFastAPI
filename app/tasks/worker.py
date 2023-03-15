from celery import Celery


class CeleryConfig:
    enable_utc = True
    broker_url = "amqp://rabbitmq:5672"
    result_backend = "rpc://"


def celery_application() -> Celery:
    celery_app = Celery("worker", broker="amqp://rabbitmq:5672", include=["app.tasks.worker"])
    celery_app.config_from_object(CeleryConfig)
    return celery_app


celery_app = celery_application()