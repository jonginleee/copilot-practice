from datetime import timezone

from fastapi import HTTPException

from app.db.session import SessionLocal
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.cart import Cart
from app.schemas.order import OrderedItem, OrderResponse


class OrderService:
    def __init__(self, cart_repository: CartRepository | None = None) -> None:
        self._cart_repo = cart_repository or CartRepository()

    def create_order(self) -> OrderResponse:
        items = self._cart_repo.get_all()
        if not items:
            raise HTTPException(status_code=400, detail="장바구니가 비어 있어 주문할 수 없습니다.")

        total_price = sum(item.subtotal for item in items)
        cart = Cart(items=items, total_price=total_price)
        db = SessionLocal()
        try:
            repo = OrderRepository(db)
            order = repo.create_order(cart=cart)
        finally:
            db.close()

        # Order is persisted, so cart can be safely cleared.
        self._cart_repo.clear()

        timestamp = order.created_at.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        ordered_items = [
            OrderedItem(
                menu_id=item.menu_id,
                name=item.name,
                category=item.category,
                image_url=item.image_url,
                price=item.price,
                quantity=item.quantity,
                subtotal=item.subtotal,
            )
            for item in items
        ]
        return OrderResponse(
            order_number=order.id,
            timestamp=timestamp,
            total_price=order.total_price,
            items=ordered_items,
        )
