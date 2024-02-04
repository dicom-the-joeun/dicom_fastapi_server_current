from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.conf.db_config import DBConfig
from app.controller.auth_ctrl import verify_user
from app.models.api_model import SelectStudyViewTab
from app.services.study_service import StudyService


router = APIRouter()
db = DBConfig()


@router.get("/", response_model=List[SelectStudyViewTab], description="Studies JSON 출력")
async def get_studies(db : Session = Depends(db.get_db), _=Depends(verify_user)):
    studies = StudyService.select_study_all(db)
    if not studies:
        raise HTTPException(status_code=404, detail="Cannot find any studies")
    return studies