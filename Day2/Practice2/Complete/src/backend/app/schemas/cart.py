from pydantic import BaseModel, Field


class CartItemRequest(BaseModel):
    menu_id: int
    quantity: int = Field(ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItem(BaseModel):
    menu_id: int
    name: str
    category: str
    image_url: str
    price: int
    quantity: int
    subtotal: int


class Cart(BaseModel):
    items: list[CartItem]
    total_price: int
