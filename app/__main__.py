from fastapi import FastAPI

from app.api.v1 import api_router
from app.gunicorn_app import StandaloneApplication
from app.middleware.middleware import middleware


app = FastAPI(middleware=middleware)


app.include_router(api_router.router,
                   prefix='/api/v1')


def run_application(app, ) -> None:
    options = {
        "bind": "%s:%s" % ("0.0.0.0", 8000),
        "worker_class": "uvicorn.workers.UvicornWorker",
        "reload": True,
        "disable_existing_loggers": False,
        "preload_app": True,
    }
    gunicorn_app = StandaloneApplication(app, options)
    gunicorn_app.run()


if __name__ == "__main__":
    run_application(app)
