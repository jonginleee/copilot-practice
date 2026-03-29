from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: int   # KRW
    quantity: int

def calculate_subtotal(items: list[LineItem]) -> int:
    return sum(i.unit_price * i.quantity for i in items)

def calculate_total(items: list[LineItem], tax_rate: float, discount_krw: int = 0) -> int:
    """
    요구사항:
    - tax_rate는 0.0~1.0(포함) 범위, 아니면 ValueError
    - discount_krw는 0 이상, 아니면 ValueError
    - 총액 = (subtotal - discount) * (1 + tax_rate)
    - subtotal - discount가 음수면 0으로 클램프
    - 최종 금액은 원 단위 정수로 반올림(round)
    """
    if not (0.0 <= tax_rate <= 1.0):
        raise ValueError("tax_rate must be between 0.0 and 1.0")
    if discount_krw < 0:
        raise ValueError("discount_krw must be >= 0")

    subtotal = calculate_subtotal(items)
    base = max(0, subtotal - discount_krw)
    return int(round(base * (1.0 + tax_rate)))
