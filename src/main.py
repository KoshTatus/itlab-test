import datetime

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi import Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from src.app.camera import Camera
from src.app.database import get_db
from src.app.db_queries import get_images_in_interval
from src.app.events import Events

app = FastAPI()
camera = Camera()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/start",
    status_code=status.HTTP_200_OK,
    description="Запускает поток в котором работает камера",
    summary="Включить камеру"
)
async def start_camera():
    if camera.running:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Camera is already running")
    camera.start()

    return {
        "msg": "Camera has been started"
    }


@app.post(
    "/stop",
    status_code=status.HTTP_200_OK,
    description="Завершает поток в котором работает камера",
    summary="Выключить камеру"
)
async def stop_camera():
    if not camera.running:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Camera isn't running")
    camera.stop()
    return {
        "msg": "Camera has been stoped"
    }


@app.get(
    "/humans",
    status_code=status.HTTP_200_OK,
    description="Возвращает записи из таблицы images, где дата добавления изображения находится в заданном диапазоне",
    summary="Фильтр по дате создания изображения",
    response_description="Список ссылок на отфильтрованные изображения"
)
async def get_humans(
        start_date: datetime.date = Query(description="Дата начала диапазона"),
        end_date: datetime.date = Query(description="Дата конца диапазона"),
        db: Session = Depends(get_db)
):
    result = get_images_in_interval(
        db=db,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "data" : result
    }


@app.get(
    "/events",
    description="Отправляет событие добавления изображения в базу данных",
    summary="SSE для отображения изображений"
)
async def events_sse(request: Request):
    return EventSourceResponse(Events.event_generator(request))


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Отображает текущие фотографии на странице",
    summary="Корень приложения"
)
async def root():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    uvicorn.run(app)
