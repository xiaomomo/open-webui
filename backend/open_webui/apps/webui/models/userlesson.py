import traceback
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text
from typing import Optional

from open_webui.apps.webui.internal.db import Base, get_db


####################
# UserLesson DB Schema
####################

class UserLesson(Base):
    __tablename__ = "userlesson"

    user_id = Column(Text, primary_key=True)
    lesson_id = Column(BigInteger, primary_key=True)
    user_content = Column(Text)
    learn_status = Column(String)


class UserLessonModel(BaseModel):
    user_id: str
    lesson_id: int
    user_content: str
    learn_status: str

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################

class UserLessonForm(BaseModel):
    user_id: str
    lesson_id: int
    user_content: str
    learn_status: str


class UserLessonTable:
    def insert_new_user_lesson(
            self, form_data: UserLessonForm
    ) -> Optional[UserLessonModel]:
        user_lesson = UserLessonModel(
            **{
                "user_id": form_data.user_id,
                "lesson_id": form_data.lesson_id,
                "user_content": form_data.user_content,
                "learn_status": form_data.learn_status,
            }
        )

        try:
            with get_db() as db:
                result = UserLesson(**user_lesson.dict())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return UserLessonModel.model_validate(result)
                else:
                    return None
        except Exception as e:
            print(f"Error creating UserLesson: {e}")
            traceback.print_exc()
            return None

    def get_user_lesson_by_id(self, user_id: int, lesson_id: int) -> Optional[UserLessonModel]:
        try:
            with get_db() as db:
                user_lesson = db.query(UserLesson).filter_by(user_id=user_id, lesson_id=lesson_id).first()
                return UserLessonModel.model_validate(user_lesson)
        except Exception:
            return None

    def get_all_user_lessons(self) -> list[UserLessonModel]:
        with get_db() as db:
            return [
                UserLessonModel.model_validate(user_lesson) for user_lesson in db.query(UserLesson).all()
            ]

    def update_user_lesson_by_id(
            self, user_id: int, lesson_id: int, form_data: UserLessonForm
    ) -> Optional[UserLessonModel]:
        try:
            with get_db() as db:
                user_lesson = db.query(UserLesson).filter_by(user_id=user_id, lesson_id=lesson_id).first()
                if user_lesson:
                    user_lesson.user_content = form_data.user_content
                    user_lesson.learn_status = form_data.learn_status
                    db.commit()
                    return UserLessonModel.model_validate(user_lesson)
                else:
                    return None
        except Exception:
            return None

    def delete_user_lesson_by_id(self, user_id: int, lesson_id: int) -> bool:
        try:
            with get_db() as db:
                db.query(UserLesson).filter_by(user_id=user_id, lesson_id=lesson_id).delete()
                db.commit()
                return True
        except Exception:
            return False


UserLessons = UserLessonTable()
