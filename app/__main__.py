from fastapi import FastAPI

from app.api.endpoints import category, product, user, login
from app.gunicorn_app import StandaloneApplication


app = FastAPI()




app.include_router(category.router,
                   prefix='/category',
                   tags=['Category'])

app.include_router(product.router,
                   prefix='/product',
                   tags=['Product'])


app.include_router(user.router,
                   prefix='/user',
                   tags=['User'])

app.include_router(login.router,
                   tags=['Login'])


def run_application(app, ) -> None:
    options = {
        "bind": "%s:%s" % ("0.0.0.0", 8080),
        "worker_class": "uvicorn.workers.UvicornWorker",
        "reload": True,
        "disable_existing_loggers": False,
        "preload_app": True,
    }
    gunicorn_app = StandaloneApplication(app, options)
    gunicorn_app.run()


if __name__ == "__main__":
    run_application(app)