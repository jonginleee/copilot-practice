from __future__ import annotations

import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[2] / "src" / "frontend" / "ui_theme.py"
spec = importlib.util.spec_from_file_location("ui_theme", module_path)
ui_theme = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(ui_theme)


get_ui_tokens = ui_theme.get_ui_tokens
build_category_guide = ui_theme.build_category_guide
resolve_menu_description = ui_theme.resolve_menu_description
build_theme_css = ui_theme.build_theme_css


def test_get_ui_tokens_uses_reference_color_family() -> None:
    tokens = get_ui_tokens()

    assert tokens["brand"] == "#5f8f2f"
    assert tokens["brand_dark"] == "#4d7728"
    assert tokens["surface"] == "#ffffff"


def test_build_category_guide_orders_categories_and_counts() -> None:
    menus = [
        {"id": 1, "category": "burger"},
        {"id": 2, "category": "burger"},
        {"id": 3, "category": "side"},
        {"id": 4, "category": "drink"},
    ]

    guide = build_category_guide(menus)

    assert [item["id"] for item in guide] == ["all", "burger", "side", "drink"]
    assert guide[0]["count"] == 4
    assert guide[1]["count"] == 2


def test_resolve_menu_description_prefers_local_override() -> None:
    menu = {"id": 1, "name": "Classic Burger", "category": "burger"}

    description = resolve_menu_description(menu)

    assert "시그니처" in description


def test_resolve_menu_description_uses_category_fallback() -> None:
    menu = {"id": 999, "name": "Temp", "category": "side"}

    description = resolve_menu_description(menu)

    assert "사이드" in description


def test_build_theme_css_contains_touch_target_and_cta_style() -> None:
    css = build_theme_css(get_ui_tokens())

    assert "--brand: #5f8f2f;" in css
    assert "--card-title: #111111;" in css
    assert ".order-cta" in css
    assert '.stButton > button[kind="primary"]' in css
    assert "min-height: 44px;" in css


def test_build_category_guide_skips_empty_category() -> None:
    menus = [
        {"id": 1, "category": "burger"},
        {"id": 2, "category": "burger"},
    ]
    guide = build_category_guide(menus)
    ids = [item["id"] for item in guide]
    assert "all" in ids
    assert "burger" in ids
    assert "side" not in ids
    assert "drink" not in ids


def test_resolve_menu_description_burger_category_fallback() -> None:
    menu = {"id": 999, "name": "Unknown Burger", "category": "burger"}
    description = resolve_menu_description(menu)
    assert "버거" in description


def test_resolve_menu_description_drink_category_fallback() -> None:
    menu = {"id": 999, "name": "Unknown Drink", "category": "drink"}
    description = resolve_menu_description(menu)
    assert "음료" in description


def test_resolve_menu_description_unknown_category_fallback() -> None:
    menu = {"id": 999, "name": "Unknown Item", "category": "dessert"}
    description = resolve_menu_description(menu)
    assert "키오스크" in description
