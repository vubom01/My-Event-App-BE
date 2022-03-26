from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.helpers.login_manager import login_required
from app.schemas.sche_base import DataResponse, ItemBaseModel
from app.schemas.sche_event import EventCreateRequest
from app.schemas.sche_user import UserDetail
from app.services.srv_event import EventService

router = APIRouter()


class UpdatePassword(ItemBaseModel):
    current_password: str
    update_password: str


@router.post('', dependencies=[Depends(login_required)])
def detail(current_user: UserDetail = Depends(login_required), request: EventCreateRequest = None,
           db: Session = Depends(deps.get_db)):
    event = EventService.create_event(db=db, event=request, user_id=current_user.id)
    return DataResponse().success_response(data=event)



