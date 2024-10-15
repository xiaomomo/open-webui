import time
from typing import Optional

from open_webui.apps.webui.internal.db import Base, get_db
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text
import traceback  # 添加这个模块来获取详细的异常堆栈信息
from datetime import datetime

####################
# Diary DB Schema
####################


class Diary(Base):
    __tablename__ = "diary"

    id = Column(String, primary_key=True)
    content = Column(Text)
    user_id = Column(String)
    contentAudio = Column(String)  # Stores the path or URL of the audio file
    sourceMaterial = Column(String)
    timestamp = Column(BigInteger)


class DiaryModel(BaseModel):
    id: str
    content: str
    user_id: str
    contentAudio: str
    sourceMaterial: str
    timestamp: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class DiaryForm(BaseModel):
    content: str
    contentAudio: str
    sourceMaterial: str


class DiaryTable:
    def insert_new_diary(
            self, user_id: str, form_data: DiaryForm
    ) -> Optional[DiaryModel]:
        diary = DiaryModel(
            **{
                "id": str(int(datetime.now().strftime("%Y%m%d"))),
                "user_id": user_id,
                "content": form_data.content,
                "contentAudio": form_data.contentAudio,
                "sourceMaterial": form_data.sourceMaterial,
                "timestamp": int(time.time()),
            }
        )

        try:
            with get_db() as db:
                result = Diary(**diary.dict())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return DiaryModel.model_validate(result)
                else:
                    return None
        except Exception as e:
            # 打印出具体的异常信息
            print(f"Error creating diary: {e}")  # 打印简短的异常信息
            traceback.print_exc()  # 打印完整的异常堆栈信息
            return None

    def get_diary_by_id(self, diary_id: str) -> Optional[DiaryModel]:
        try:
            with get_db() as db:
                diary = db.query(Diary).filter_by(id=diary_id).first()
                return DiaryModel.model_validate(diary)
        except Exception:
            return None

    def get_all_diaries(self) -> list[DiaryModel]:
        with get_db() as db:
            return [
                DiaryModel.model_validate(diary) for diary in db.query(Diary).all()
            ]

    def update_diary_by_id(
            self, diary_id: str, form_data: DiaryForm
    ) -> Optional[DiaryModel]:
        try:
            with get_db() as db:
                diary = db.query(Diary).filter_by(id=diary_id).first()
                diary.content = form_data.content
                diary.contentAudio = form_data.contentAudio
                diary.sourceMaterial = form_data.sourceMaterial
                diary.timestamp = int(time.time())
                db.commit()
                return DiaryModel.model_validate(diary)
        except Exception:
            return None

    def delete_diary_by_id(self, diary_id: str) -> bool:
        try:
            with get_db() as db:
                db.query(Diary).filter_by(id=diary_id).delete()
                db.commit()

                return True
        except Exception:
            return False


Diaries = DiaryTable()