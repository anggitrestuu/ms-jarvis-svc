from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.endpoints.deps import CurrentUser, get_current_user
from app.models.enums import StatusEnum
from app.services.bot import BotService
from app.utils.response_handler import response
from uuid import UUID

router = APIRouter()


@router.get("/discoveries")
async def get_discovery_characters(
    service: BotService = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    category_id: Optional[UUID] = Query(None),
    name: Optional[str] = Query(None),
    current_user: CurrentUser = Depends(get_current_user),
):
    filters = {"status": StatusEnum.ACTIVE}
    if category_id:
        filters["category_id"] = category_id
    
    search_fields = {"name": "contains"}
    search_term = None
    if name:
        search_term = name
    
    items, total = await service.get_bots(
        filters=filters,
        skip=skip,
        limit=limit,
        search_term=search_term,
        search_fields=search_fields
    )
    return response.success(data=items, message="Character fetched successfully", meta={"total": total})

@router.get("/recents")
async def get_recents_characters(
    service: BotService = Depends(),
    current_user: CurrentUser = Depends(get_current_user),
):
    item = await service.get_bots(filters={"status": StatusEnum.ACTIVE}, skip=0, limit=10)
    return response.success(data=item, message="Character fetched successfully")

@router.get("/{bot_id}")
async def get_character(
    bot_id: UUID,
    service: BotService = Depends(),
    current_user: CurrentUser = Depends(get_current_user),
):
    items, total = await service.get_bot(bot_id, with_details=False)
    return response.success(data=items, message="Character fetched successfully", meta={"total": total})