from sqlalchemy.orm import Mapped, mapped_column
import datetime

from src.app.database import Base


class ImagesOrm(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True, name="id")
    filePath: Mapped[str] = mapped_column(name="file_path")
    createdAt: Mapped[datetime.datetime] = mapped_column(name="created_at", default=datetime.datetime.now())