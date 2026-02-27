from fastapi import APIRouter
from .register import register_user
from .basic import login_user, user_profile_update, profile_delete


from database import db_dep
from dependencies.dependencies import current_user_basic_dep
from schemas import (
    UserProfileResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


router.add_api_route("/register", register_user, methods=["POST"])
router.add_api_route("/login", login_user, methods=["POST"])
router.add_api_route("/profile/update", user_profile_update, methods=["PUT"])
router.add_api_route("/profile/delete", profile_delete, methods=["DELETE"])


@router.get("/profile/", response_model=UserProfileResponse)
async def user_profile(db: db_dep, current_user: current_user_basic_dep):
    return current_user
