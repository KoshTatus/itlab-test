import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.app.models import ImagesOrm
from src.app.schemas import Image


def get_all_images(db: Session) -> list[str]:
    query = text("""
        SELECT * FROM images
    """)
    result = [Image.model_validate(row, from_attributes=True).filePath for row in db.execute(query).all()]
    return result

def get_images_in_interval(
        db: Session,
        start_date: datetime.date,
        end_date: datetime.date
):
    query = text("""
        SELECT * FROM images WHERE created_at BETWEEN :start_date AND :end_date
    """)
    params = {
        "start_date" : start_date,
        "end_date" : end_date
    }

    result = [Image.model_validate(row, from_attributes=True).filePath for row in db.execute(query, params).all()]
    return result

def add_image(db: Session, image: Image):
    new_image = ImagesOrm(**image.model_dump())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
