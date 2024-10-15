from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from open_webui.apps.webui.models.diary import DiaryForm, DiaryModel, Diaries
from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.utils import get_admin_user, get_verified_user
import logging

log = logging.getLogger(__name__)
router = APIRouter()

############################
# GetDiaries
############################

@router.get("/", response_model=list[DiaryModel])
async def get_diaries(user=Depends(get_verified_user)):
    return Diaries.get_all_diaries()


############################
# CreateNewDiary
############################

@router.post("/create", response_model=Optional[DiaryModel])
async def create_new_diary(form_data: DiaryForm, user=Depends(get_admin_user)):
    print(f"test create_new_diary form_data:{form_data}")
    diary = Diaries.insert_new_diary(user.id, form_data)

    if diary:
        return diary
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(),
    )

@router.post("/create_test")
async def create_new_diary_test(user=Depends(get_admin_user)):
    print("test create_new_diary_test")
    return "123"


############################
# GetDiaryById
############################

@router.get("/{diary_id}", response_model=Optional[DiaryModel])
async def get_diary_by_id(diary_id: str):
    diary = Diaries.get_diary_by_id(diary_id)

    if diary:
        return diary
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateDiaryById
############################

@router.post("/{diary_id}/update", response_model=Optional[DiaryModel])
async def update_diary_by_id(
        diary_id: str,
        form_data: DiaryForm,
        user=Depends(get_admin_user),
):
    diary = Diaries.update_diary_by_id(diary_id, form_data)

    if diary:
        return diary
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )


############################
# DeleteDiaryById
############################

@router.delete("/{diary_id}/delete", response_model=bool)
async def delete_diary_by_id(diary_id: str, user=Depends(get_admin_user)):
    result = Diaries.delete_diary_by_id(diary_id)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ERROR_MESSAGES.NOT_FOUND,
    )