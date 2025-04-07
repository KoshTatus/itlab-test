import asyncio
from fastapi import Request


class Events:
    STREAM_DELAY = 1
    CURRENT_IMAGE_PATH = None

    @classmethod
    def change_image_path(cls, image_path: str):
        cls.CURRENT_IMAGE_PATH = image_path

    @classmethod
    async def event_generator(cls, request: Request):
        while True:
            if await request.is_disconnected():
                break
            if cls.CURRENT_IMAGE_PATH:
                yield {
                    "data" : cls.CURRENT_IMAGE_PATH
                }
                cls.CURRENT_IMAGE_PATH = None
            await asyncio.sleep(cls.STREAM_DELAY)
