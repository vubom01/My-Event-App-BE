from fastapi import APIRouter, Depends

from app.helpers.login_manager import login_required
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserDetailResponse
from app.services.srv_user import UserService

router = APIRouter()


@router.get('/me', dependencies=[Depends(login_required)], response_model=DataResponse[UserDetailResponse])
def detail(current_user: UserDetailResponse = Depends(UserService.get_current_user)):
    return DataResponse().success_response(data=current_user)


