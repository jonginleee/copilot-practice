from fastapi import APIRouter

from app.schemas.cart import Cart, CartItemRequest, CartItemUpdate
from app.services.cart_service import CartService

router = APIRouter(tags=["cart"])
cart_service = CartService()


@router.post("/cart/items", response_model=Cart)
def add_item(body: CartItemRequest) -> Cart:
    return cart_service.add_item(body)


@router.put("/cart/items/{menu_id}", response_model=Cart)
def update_item(menu_id: int, body: CartItemUpdate) -> Cart:
    return cart_service.update_item(menu_id, body.quantity)


@router.delete("/cart/items/{menu_id}", response_model=Cart)
def remove_item(menu_id: int) -> Cart:
    return cart_service.remove_item(menu_id)


@router.get("/cart", response_model=Cart)
def get_cart() -> Cart:
    return cart_service.get_cart()


@router.delete("/cart", response_model=Cart)
def clear_cart() -> Cart:
    return cart_service.clear_cart()
