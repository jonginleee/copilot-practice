import pytest

from src.calculator import calculate_discount, divide, normalize_name


def test_divide_zero_numerator_returns_zero():
	assert divide(0, 5) == 0


def test_divide_negative_numbers():
	assert divide(-10, 2) == -5
	assert divide(-10, -2) == 5


def test_divide_by_zero_raises_error():
	with pytest.raises(ZeroDivisionError):
		divide(10, 0)


def test_divide_invalid_type_raises_type_error():
	with pytest.raises(TypeError):
		divide("10", 2)


def test_calculate_discount_zero_rate_returns_original_price():
	assert calculate_discount(100, 0) == 100


def test_calculate_discount_full_rate_returns_zero():
	assert calculate_discount(100, 1) == 0


def test_calculate_discount_rate_over_one_returns_negative_value():
	assert calculate_discount(100, 1.5) == -50


def test_calculate_discount_negative_rate_increases_price():
	assert calculate_discount(100, -0.1) == 110


def test_calculate_discount_invalid_type_raises_type_error():
	with pytest.raises(TypeError):
		calculate_discount("100", 0.1)


def test_normalize_name_empty_string_returns_empty_string():
	assert normalize_name("") == ""


def test_normalize_name_trims_and_title_cases():
	assert normalize_name("  aLiCe joHNson  ") == "Alice Johnson"


def test_normalize_name_handles_non_ascii():
	assert normalize_name("  hONG gILDONG 김철수  ") == "Hong Gildong 김철수"


def test_normalize_name_invalid_type_raises_attribute_error():
	with pytest.raises(AttributeError):
		normalize_name(None)
