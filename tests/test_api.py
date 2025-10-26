import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from decimal import Decimal
from schemas import CalculationsSchema
from main import app
from router import (calculate_s, calculate_l, price_l, price_s, main_calculation)

@pytest.mark.asyncio
async def test_index():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
       response = await ac.get("/")
       assert response.status_code == 200

@pytest.mark.asyncio
async def test_Calculations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
       response = await ac.get("/")
       assert response.status_code == 200

@pytest.mark.asyncio
async def test_calculate_s():
    # Фракция 0-1
    result = await calculate_s(10, "0-1")
    assert result == 10, "Расход мешков 1:1"

    # Фракция 3-6
    result = await calculate_s(20, "3-6")
    assert result == 30, "Расход мешков 1:1.5"

    # Фракция 5-10
    result = await calculate_s(30, "5-10")
    assert result == 60, "Расход мешков 1:2"

@pytest.mark.asyncio
async def test_calculate_l():
    # Фракция 0-2
    result = await calculate_l(10, "0-2")
    assert result == 10, "Расход мешков 1:1"

    # Фракция 3-6
    result = await calculate_l(20, "3-6")
    assert result == 30, "Расход мешков 1:1.5"

    # Фракция 10+
    result = await calculate_l(30, "10+")
    assert result == 60, "Расход мешков 1:2"

# Используем фикстуру для инициализации TestClient
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# Тестирование успешной операции
@pytest.mark.asyncio
async def test_calculations_success(client):
    # Данные для успешного расчета
    form_data = {
        "square": 100.0,
        "fraction": "0-1",
        "type_m": "С"
    }

    # Отправляем POST-запрос
    response = client.post("/Calculations", data=form_data)

    # Проверяем успешный статус-код
    assert response.status_code == 200

    # Проверяем наличие ключевых элементов в ответе
    content = response.text
    assert "Мульчи понадобиться: 100.0 мешков." in content
    assert "Стоймость составит: 27000.0 руб." in content