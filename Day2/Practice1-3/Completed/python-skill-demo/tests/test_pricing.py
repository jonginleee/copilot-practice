from src.pricing import apply_discount


def test_apply_discount_rounds_to_two_decimals():
    assert apply_discount(19.99, 0.15) == 16.99