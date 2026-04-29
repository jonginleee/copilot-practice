from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_menus() -> None:
    response = client.get("/menus")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_on_startup_calls_init_db() -> None:
    from app.main import on_startup

    on_startup()  # should not raise


def test_menu_list_filter_by_category() -> None:
    from app.repositories.menu_repository import MenuRepository

    repo = MenuRepository()
    burgers = repo.list_menus(category="burger")
    assert len(burgers) >= 1
    assert all(item.category.lower() == "burger" for item in burgers)
