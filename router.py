import asyncio
from fastapi import APIRouter, Request, Form, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import math
from typing import Annotated  # Аннотации типов
from schemas import CalculationsSchema  # Валидная схема для расчётов

# Создание роутера для организации путей
router = APIRouter(tags=["Остальные страницы приложения"])

templates = Jinja2Templates(directory="templates")


@router.get("/Calculations", response_class=HTMLResponse, tags=["Расчёты"])
async def Calculations(request: Request, id: int | None = None):
    """
    Показывает страницу расчётов пользователям.
    :param request: HTTP-запрос.
    :param id: Необязательный параметр.
    :return: Рендер шаблона 'Calculations.html'.
    """
    return templates.TemplateResponse("Calculations.html", {"request": request})


async def calculate_s(square: float, fraction: str) -> float:
    """Рассчитать кол-во мульчи сосны на площадь."""
    match fraction:
        case "0-1" | "0-7" | "1-5":
            return square * 1
        case "2-4" | "3-6":
            return square * 1.5
        case "5-7" | "5-10":
            return square * 2
        case _:
            return 0


async def calculate_l(square: float, fraction: str) -> float:
    """Рассчитать кол-во мульчи лиственницы на площадь."""
    match fraction:
        case "0-2" | "2-4":
            return square * 1
        case "3-6":
            return square * 1.5
        case "6-10" | "10+":
            return square * 2
        case _:
            return 0


async def price_total_s(s_clak: float, fraction: str, s_clak2: float, fraction2: str) -> float:
    """Общая функция для расчета общей цены с учетом обоих видов фракций"""
    prices = {
        "0-1": 270,
        "0-7": 300,
        "1-5": 370,
        "2-4": 470,
        "3-6": 510,
        "5-7": 530,
        "5-10": 750,
    }

    total_price = (
            s_clak * prices.get(fraction, 0) +
            s_clak2 * prices.get(fraction2, 0)
    )
    return total_price


async def price_total_l(l_clak: float, fraction: str, l_clak2: float, fraction2: str) -> float:
    """Общая функция для расчета общей цены с учетом обоих видов фракций"""
    prices = {
        "0-2": 430,
        "2-4": 490,
        "3-6": 530,
        "6-10": 550,
        "10+": 600
    }

    total_price = (
            l_clak * prices.get(fraction, 0) +
            l_clak2 * prices.get(fraction2, 0)
    )
    return total_price


# Основная функция расчета
async def main_calculation(data: CalculationsSchema) -> dict[str, float]:
    # Получаем исходные данные
    square = data.square
    fraction = data.fraction
    fraction2 = data.fraction2
    type_m = data.type_m

    # 1. Рассчитываем мульчу сосны
    s_clak = await calculate_s(square, fraction)
    s_clak2 = await calculate_s(square, fraction2)
    l_clak = await calculate_l(square, fraction)
    l_clak2 = await calculate_l(square, fraction2)
    s_price = await price_total_s(s_clak, fraction, s_clak2, fraction2)
    l_price = await price_total_l(l_clak, fraction, l_clak2, fraction2)

    # 2. Округляем результаты до 3-х знаков после запятой
    rounded_s_clak = round(s_clak, 3)
    rounded_s_clak2 = round(s_clak2, 3)
    rounded_l_clak = round(l_clak, 3)
    rounded_l_clak2 = round(l_clak2, 3)
    rounded_s_price = round(s_price, 3)
    rounded_l_price = round(l_price, 3)

    result = {}
    if type_m == "С":
        result['square_mulch'] = rounded_s_clak
        result['square_mulch2'] = rounded_s_clak2
        result['price'] = rounded_s_price
    elif type_m == "Л":
        result['square_mulch'] = rounded_l_clak
        result['square_mulch2'] = rounded_l_clak2
        result['price'] = rounded_l_price
    else:
        raise HTTPException(status_code=400, detail="Тип материала указан неверно.")

    return result


@router.post("/Calculations", tags=["Расчёты"])
async def calculations_post(
        request: Request,
        square: float = Form(...),
        fraction: str = Form(...),
        fraction2: str = Form(...),
        type_m: str = Form(...)
):
    """
    Обрабатывает POST-запрос на странице калькулятора и производит расчёт необходимых материалов.

    Параметры:
    `request`: объект HTTP-запроса.
    Остальные аргументы получают данные из формы.

    Возвращаемое значение:
    рендер шаблона 'Calculations.html', содержащий рассчитанные данные.
    """

    try:
        data = CalculationsSchema(
            square=square,
            fraction=fraction,
            fraction2=fraction2,
            type_m=type_m,
        )

        # Вызываем основную функцию расчета и получаем результат
        result = await main_calculation(data)

        return templates.TemplateResponse(
            request, "Calculations.html", context={**{"request": request}, **result}
        )
    except HTTPException as e:
        return templates.TemplateResponse(
            "Calculations.html", {"request": request, "error": e.detail}
        )