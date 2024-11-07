import time
from typing import Optional

from open_webui.apps.webui.internal.db import Base, get_db
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text
import traceback
from datetime import datetime

####################
# FredisaLesson DB Schema
####################

class FredisaLesson(Base):
    __tablename__ = "fredisalesson"

    id = Column(String, primary_key=True)
    unit = Column(String)
    content = Column(Text)
    lesson_json = Column(Text)

class FredisaLessonModel(BaseModel):
    id: str
    unit: str
    content: str
    lesson_json: str

    model_config = ConfigDict(from_attributes=True)

####################
# Forms
####################

class FredisaLessonForm(BaseModel):
    unit: str
    content: str
    lesson_json: str

class FredisaLessonTable:
    def insert_new_lesson(
            self, form_data: FredisaLessonForm
    ) -> Optional[FredisaLessonModel]:
        lesson = FredisaLessonModel(
            **{
                "id": str(int(datetime.now().strftime("%Y%m%d%H%M%S"))),
                "unit": form_data.unit,
                "content": form_data.content,
                "lesson_json": form_data.lesson_json
            }
        )

        try:
            with get_db() as db:
                result = FredisaLesson(**lesson.dict())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return FredisaLessonModel.model_validate(result)
                else:
                    return None
        except Exception as e:
            print(f"Error creating FredisaLesson: {e}")
            traceback.print_exc()
            return None

    def get_lesson_by_id(self, lesson_id: str) -> Optional[FredisaLessonModel]:
        try:
            with get_db() as db:
                lesson = db.query(FredisaLesson).filter_by(id=lesson_id).first()
                return FredisaLessonModel.model_validate(lesson)
        except Exception:
            return None

    def get_all_lessons(self) -> list[FredisaLessonModel]:
        with get_db() as db:
            return [
                FredisaLessonModel.model_validate(lesson) for lesson in db.query(FredisaLesson).all()
            ]

    def update_lesson_by_id(
            self, lesson_id: str, form_data: FredisaLessonForm
    ) -> Optional[FredisaLessonModel]:
        try:
            with get_db() as db:
                lesson = db.query(FredisaLesson).filter_by(id=lesson_id).first()
                lesson.unit = form_data.unit
                lesson.content = form_data.content
                db.commit()
                return FredisaLessonModel.model_validate(lesson)
        except Exception:
            return None

    def delete_lesson_by_id(self, lesson_id: str) -> bool:
        try:
            with get_db() as db:
                db.query(FredisaLesson).filter_by(id=lesson_id).delete()
                db.commit()

                return True
        except Exception:
            return False


FredisaLessons = FredisaLessonTable()