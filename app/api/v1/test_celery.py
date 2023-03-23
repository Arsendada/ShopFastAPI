from fastapi import APIRouter

from app.services.tasks.tasks import test_celery_start


router = APIRouter()


@router.post("/test-celery/", status_code=201)
def test_celery(
        value: int
):
    task = test_celery_start.delay(value)
    return {"msg": task.get()}
