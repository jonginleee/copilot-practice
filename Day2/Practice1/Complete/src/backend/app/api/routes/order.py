from fastapi import APIRouter

from app.schemas.order import OrderResponse
from app.services.order_service import OrderService

router = APIRouter(tags=["orders"])
order_service = OrderService()


@router.post("/orders", response_model=OrderResponse)
def create_order() -> OrderResponse:
    return order_service.create_order()
