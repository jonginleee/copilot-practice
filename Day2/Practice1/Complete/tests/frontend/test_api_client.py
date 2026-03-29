from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

module_path = Path(__file__).resolve().parents[2] / "src" / "frontend" / "api_client.py"
spec = importlib.util.spec_from_file_location("api_client", module_path)
api_client = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(api_client)

ApiClientError = api_client.ApiClientError
_map_error_message = api_client._map_error_message
add_cart_item = api_client.add_cart_item
create_order = api_client.create_order


def _mock_response(status_code: int, payload: dict | None = None) -> Mock:
    response = Mock()
    response.status_code = status_code
    if payload is None:
        response.json.side_effect = ValueError("no json")
    else:
        response.json.return_value = payload
    return response


def test_map_error_message_400_with_detail() -> None:
    response = _mock_response(400, {"detail": "품절된 메뉴입니다."})
    assert _map_error_message(response) == "품절된 메뉴입니다."


def test_map_error_message_422() -> None:
    response = _mock_response(422, {"detail": "invalid"})
    assert _map_error_message(response) == "입력값을 확인해주세요."


def test_add_cart_item_raises_api_client_error_on_404() -> None:
    response = _mock_response(404, {"detail": "메뉴를 찾을 수 없습니다."})
    with patch.object(api_client.requests, "request", return_value=response):
        with pytest.raises(ApiClientError) as exc_info:
            add_cart_item(999, 1)

    assert exc_info.value.status_code == 404
    assert "메뉴를 찾을 수 없습니다." in str(exc_info.value)


def test_create_order_success() -> None:
    response = _mock_response(
        200,
        {
            "order_number": 1,
            "timestamp": "2026-03-29T10:00:00Z",
            "total_price": 13000,
            "items": [],
        },
    )
    with patch.object(api_client.requests, "request", return_value=response):
        payload = create_order()

    assert payload["order_number"] == 1
    assert payload["timestamp"].endswith("Z")
