from pydantic import BaseModel # Импортируем базовые классы и инструменты Pydantic

class CalculationsSchema(BaseModel):
    """
    Модель данных для расчётов
    """
    square: float | None
    fraction: str | None
    type_m: str | None