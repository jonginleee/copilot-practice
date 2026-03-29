import json
from pathlib import Path

import streamlit as st

from api_client import (
	ApiClientError,
	add_cart_item,
	clear_cart,
	create_order,
	get_cart,
	remove_cart_item,
	update_cart_item,
)
from ui_theme import build_category_guide, build_theme_css, get_ui_tokens, resolve_menu_description

st.set_page_config(page_title="주문", layout="wide")


def load_menus() -> list[dict]:
	data_file = Path(__file__).resolve().parents[1] / "backend" / "app" / "data" / "sample_menus.json"
	with data_file.open("r", encoding="utf-8") as fp:
		return json.load(fp)


def init_state() -> None:
	if "quantities" not in st.session_state:
		st.session_state.quantities = {}
	if "active_category" not in st.session_state:
		st.session_state.active_category = "all"
	if "cart" not in st.session_state:
		st.session_state.cart = {"items": [], "total_price": 0}
	if "flash_error" not in st.session_state:
		st.session_state.flash_error = ""
	if "flash_success" not in st.session_state:
		st.session_state.flash_success = ""
	if "last_order_number" not in st.session_state:
		st.session_state.last_order_number = 0
	if "last_order" not in st.session_state:
		st.session_state.last_order = None


def refresh_cart() -> None:
	st.session_state.cart = get_cart()


def format_price(price: int) -> str:
	return f"{price:,}원"


def apply_reference_theme() -> None:
	tokens = get_ui_tokens()
	st.markdown(build_theme_css(tokens), unsafe_allow_html=True)


def render_top_navigation() -> None:
	nav_cols = st.columns([1, 5, 2])
	with nav_cols[0]:
		if _LOGO_PATH.exists():
			st.image(str(_LOGO_PATH), width=72)
		else:
			st.markdown("### KIOSK")

	with nav_cols[1]:
		st.markdown(
			"""
			<div class="top-nav">
			  <span class="menu-item">OUR VALUES</span>
			  <span class="menu-item active">MENU</span>
			  <span class="menu-item">LOCATIONS</span>
			  <span class="menu-item">NEWS & EVENT</span>
			</div>
			""",
			unsafe_allow_html=True,
		)

	with nav_cols[2]:
		st.markdown('<div style="text-align:right;"><span class="order-cta">Order Now</span></div>', unsafe_allow_html=True)

def get_filtered_menus(menus: list[dict]) -> list[dict]:
	active = st.session_state.active_category
	if active == "all":
		return menus
	return [menu for menu in menus if menu.get("category") == active]


def render_category_rail(menus: list[dict]) -> None:
	st.markdown('<div class="category-rail">', unsafe_allow_html=True)
	for category in build_category_guide(menus):
		is_active = st.session_state.active_category == category["id"]
		button_type = "primary" if is_active else "secondary"
		if st.button(
			category["label"],
			key=f"cat_{category['id']}",
			type=button_type,
			use_container_width=True,
		):
			st.session_state.active_category = category["id"]
			st.rerun()
		st.caption(f"{category['marker']} · {category['count']} items")
	st.markdown("</div>", unsafe_allow_html=True)


def render_menu_grid(menus: list[dict]) -> None:
	if not menus:
		st.info("표시할 메뉴가 없습니다.")
		return

	columns = st.columns(3)
	for idx, menu in enumerate(menus):
		col = columns[idx % 3]
		sold_out = menu.get("is_sold_out", False)
		status_label = "SOLD OUT" if sold_out else "AVAILABLE"
		status_class = "sold-out" if sold_out else "available"

		with col:
			try:
				st.image(menu["image_url"], use_container_width=True)
			except Exception:
				pass

			description = resolve_menu_description(menu)
			st.markdown(
				f"""
				<div class="menu-card">
					<div class="title">
						{menu['name']}
					</div>
					<div style="font-size: 13px; color: #6e7477; margin-bottom: 10px; font-weight: 700;">
						#{menu['id']} · {menu['category']}
					</div>
					<div style="font-size: 16px; color: #6e7477; min-height: 48px; margin-bottom: 10px;">
						{description}
					</div>
					<div class="price">
						{format_price(menu['price'])}
					</div>
					<div class="status {status_class}">
						{status_label}
					</div>
				</div>
				""",
				unsafe_allow_html=True,
			)

			qty_key = f"qty_{menu['id']}"
			if qty_key not in st.session_state.quantities:
				st.session_state.quantities[qty_key] = 1

			quantity = st.number_input(
				f"수량 ({menu['name']})",
				min_value=1,
				value=int(st.session_state.quantities[qty_key]),
				step=1,
				key=qty_key,
				label_visibility="collapsed",
			)
			st.session_state.quantities[qty_key] = int(quantity)

			if st.button(
				"구매하기",
				key=f"add_{menu['id']}",
				disabled=sold_out,
				use_container_width=True,
			):
				try:
					st.session_state.cart = add_cart_item(menu["id"], int(quantity))
					st.session_state.flash_success = f"{menu['name']} {quantity}개를 담았습니다."
					st.session_state.flash_error = ""
					st.rerun()
				except ApiClientError as exc:
					st.session_state.flash_error = str(exc)
					st.session_state.flash_success = ""
					st.rerun()


def render_cart_panel() -> None:
	st.markdown('<div class="cart-panel-title">주문 내역</div>', unsafe_allow_html=True)
	cart = st.session_state.cart
	items = cart.get("items", [])

	if not items:
		st.info("장바구니가 비어 있습니다.")
		return

	for item in items:
		with st.container(border=True):
			st.write(f"**{item['name']}**")
			st.caption(f"단가 {format_price(item['price'])} · 소계 {format_price(item['subtotal'])}")

			control_cols = st.columns([2, 1, 1])
			new_qty = control_cols[0].number_input(
				f"수량-{item['menu_id']}",
				min_value=1,
				value=int(item["quantity"]),
				step=1,
				key=f"cart_qty_{item['menu_id']}",
				label_visibility="collapsed",
			)

			if control_cols[1].button("수정", key=f"update_{item['menu_id']}", use_container_width=True):
				try:
					st.session_state.cart = update_cart_item(item["menu_id"], int(new_qty))
					st.session_state.flash_success = "수량을 변경했습니다."
					st.session_state.flash_error = ""
					st.rerun()
				except ApiClientError as exc:
					st.session_state.flash_error = str(exc)
					st.session_state.flash_success = ""
					st.rerun()

			if control_cols[2].button("삭제", key=f"remove_{item['menu_id']}", use_container_width=True):
				try:
					st.session_state.cart = remove_cart_item(item["menu_id"])
					st.session_state.flash_success = "항목을 삭제했습니다."
					st.session_state.flash_error = ""
					st.rerun()
				except ApiClientError as exc:
					st.session_state.flash_error = str(exc)
					st.session_state.flash_success = ""
					st.rerun()

	st.markdown(f"### 총액: {format_price(int(cart.get('total_price', 0)))}")

	action_cols = st.columns(2)
	if action_cols[0].button("장바구니 비우기", use_container_width=True):
		try:
			st.session_state.cart = clear_cart()
			st.session_state.flash_success = "장바구니를 비웠습니다."
			st.session_state.flash_error = ""
			st.rerun()
		except ApiClientError as exc:
			st.session_state.flash_error = str(exc)
			st.session_state.flash_success = ""
			st.rerun()

	if action_cols[1].button("주문하기", use_container_width=True, type="primary"):
		if not items:
			st.session_state.flash_error = "장바구니가 비어 있어 주문할 수 없습니다."
			st.session_state.flash_success = ""
			st.rerun()
		try:
			st.session_state.last_order = create_order()
			st.session_state.cart = {"items": [], "total_price": 0}
			st.session_state.flash_success = "주문이 완료되었습니다."
			st.session_state.flash_error = ""
			st.rerun()
		except ApiClientError as exc:
			st.session_state.flash_error = str(exc)
			st.session_state.flash_success = ""
			st.rerun()


def render_order_result() -> None:
	order = st.session_state.last_order
	if not order:
		return

	with st.container(border=True):
		st.success("결제가 모의 완료되었습니다.")
		st.write(f"주문번호: {order['order_number']}")
		st.write(f"주문시각: {order['timestamp']}")
		st.write(f"결제금액: {format_price(order['total_price'])}")


_LOGO_PATH = Path(__file__).resolve().parents[2] / "resources" / "burger_logo.png"


def main() -> None:
	apply_reference_theme()
	render_top_navigation()

	all_menus = load_menus()
	init_state()

	try:
		refresh_cart()
	except ApiClientError as exc:
		st.error(f"장바구니 API 연결 실패: {exc}")

	if st.session_state.flash_error:
		st.error(st.session_state.flash_error)
	if st.session_state.flash_success:
		st.success(st.session_state.flash_success)

	rail_col, menu_col, cart_col = st.columns([0.9, 4.4, 2.2])

	with rail_col:
		render_category_rail(all_menus)

	with menu_col:
		st.markdown('<div style="font-size:40px;font-weight:900;margin-bottom:4px;">BURGERS</div>', unsafe_allow_html=True)
		st.markdown(
			"<div style='color:#6e7477;font-size:18px;margin-bottom:16px;'>신선한 재료와 균형 잡힌 조합으로 준비한 메뉴를 선택해 주세요.</div>",
			unsafe_allow_html=True,
		)
		render_menu_grid(get_filtered_menus(all_menus))

	with cart_col:
		render_cart_panel()
		render_order_result()


main()
