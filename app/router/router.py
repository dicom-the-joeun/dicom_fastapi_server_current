from fastapi import APIRouter

from app.controller import (auth_ctrl, study_ctrl, dcm_ctrl)


router = APIRouter()

router.include_router(
    auth_ctrl.router,
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    dcm_ctrl.router,
    prefix="/dcms",
    tags=["dcms"]
)

router.include_router(
    study_ctrl.router,
    prefix="/studies",
    tags=["studies"]
)

router.include_router(
    study_ctrl.router,
    prefix="/test",
    tags=["test"]
)