from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessonModel, FredisaLessons
from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.utils import get_admin_user, get_verified_user
import logging

log = logging.getLogger(__name__)
router = APIRouter()

############################
# GetFredisaLessons
############################

@router.get("/fredisalessons", response_model=list[FredisaLessonModel])
async def get_fredisa_lessons():
    return FredisaLessons.get_all_lessons()


############################
# CreateNewFredisaLesson
############################

@router.post("/fredisalessons/create", response_model=Optional[FredisaLessonModel])
async def create_new_fredisa_lesson(form_data: FredisaLessonForm, user=Depends(get_admin_user)):
    print(f"test create_new_fredisa_lesson form_data:{form_data}")
    lesson = FredisaLessons.insert_new_lesson(form_data)

    if lesson:
        return lesson
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(),
    )


############################
# GetFredisaLessonById
############################

@router.get("/fredisalessons/{lesson_id}", response_model=Optional[FredisaLessonModel])
async def get_fredisa_lesson_by_id(lesson_id: str):
    lesson = FredisaLessons.get_lesson_by_id(lesson_id)
    print(f"test get_fredisa_lesson_by_id lesson:{lesson}")
    if lesson:
        return lesson
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateFredisaLessonById
############################

@router.post("/fredisalessons/{lesson_id}/update", response_model=Optional[FredisaLessonModel])
async def update_fredisa_lesson_by_id(
        lesson_id: str,
        form_data: FredisaLessonForm,
        user=Depends(get_admin_user),
):
    lesson = FredisaLessons.update_lesson_by_id(lesson_id, form_data)

    if lesson:
        return lesson
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )


############################
# DeleteFredisaLessonById
############################

@router.delete("/fredisalessons/{lesson_id}/delete", response_model=bool)
async def delete_fredisa_lesson_by_id(lesson_id: str, user=Depends(get_admin_user)):
    result = FredisaLessons.delete_lesson_by_id(lesson_id)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ERROR_MESSAGES.NOT_FOUND,
    )