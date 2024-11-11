from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from open_webui.apps.webui.models.userlesson import UserLessonForm, UserLessonModel, UserLessons
from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.utils import get_admin_user, get_verified_user
import logging

log = logging.getLogger(__name__)
router = APIRouter()

############################
# GetUserLessons
############################

@router.get("/userlessons", response_model=list[UserLessonModel])
async def get_user_lessons(user=Depends(get_verified_user)):
    return UserLessons.get_all_user_lessons()

############################
# CreateNewUserLesson
############################

@router.post("/userlessons/create", response_model=Optional[UserLessonModel])
async def create_new_user_lesson(form_data: UserLessonForm, user=Depends(get_verified_user)):

    form_data.user_id=user.id
    print(f"test create_new_user_lesson form_data:{form_data}")
    lesson = UserLessons.insert_new_user_lesson(form_data)

    if lesson:
        return lesson
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(),
    )


############################
# GetUserLessonById
############################

@router.get("/userlessons/{lesson_id}", response_model=Optional[UserLessonModel])
async def get_user_lesson_by_id(lesson_id: str):
    lesson = UserLessons.get_lesson_by_id(lesson_id)

    if lesson:
        return lesson
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateUserLessonById
############################

@router.post("/userlessons/{lesson_id}/update", response_model=Optional[UserLessonModel])
async def update_user_lesson_by_id(
        lesson_id: str,
        form_data: UserLessonForm,
        user=Depends(get_admin_user),
):
    lesson = UserLessons.update_lesson_by_id(lesson_id, form_data)

    if lesson:
        return lesson
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )


############################
# DeleteUserLessonById
############################

@router.delete("/userlessons/{lesson_id}/delete", response_model=bool)
async def delete_user_lesson_by_id(lesson_id: str, user=Depends(get_admin_user)):
    result = UserLessons.delete_lesson_by_id(lesson_id)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ERROR_MESSAGES.NOT_FOUND,
    )
