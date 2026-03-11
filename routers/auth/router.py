from fastapi import APIRouter
from database import db_dep
from schemas.auth import UserProfileResponse

from .register import register_user
from .session import router as session_router
from .basic import login_user, user_profile_update, profile_delete
from dependencies.dependencies import session_auth_dep

router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(session_router)


@router.post("/login", response_model=None)
async def login(db: db_dep, login_data=None):
    return await login_user(db, login_data)


# 4. Profil funksiyasini to'g'rilang
@router.get("/profile/", response_model=UserProfileResponse)
async def user_profile(db: db_dep, current_user: session_auth_dep):
    return current_user


router.add_api_route("/register", register_user, methods=["POST"])
router.add_api_route("/login", login_user, methods=["POST"])
router.add_api_route("/profile/update", user_profile_update, methods=["PUT"])
router.add_api_route("/profile/delete", profile_delete, methods=["DELETE"])
