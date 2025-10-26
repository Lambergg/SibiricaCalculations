from fastapi import FastAPI, Request # Подключаем основной класс FastAPI и класс Request
from fastapi.responses import HTMLResponse # Используем HTMLResponse для возврата HTML-контента
from fastapi.staticfiles import StaticFiles # Для обслуживания статических файлов
from fastapi.templating import Jinja2Templates # Шаблонизатор Jinja2 для рендеринга шаблонов
import uvicorn # Сервер Uvicorn для запуска приложения
from router import router as other_routres # Импортируем роутер маршрутов

# Импортируем роутер маршрутов
app = FastAPI(title="Сибирица. Калькулятор мульчи")

app.openapi_schema = None

# Импортируем роутер маршрутов
app.include_router(other_routres)

# Монтируем каталог static для предоставления статических ресурсов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка шаблонизатора Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, tags=["Главная страница!"])
async def index(request: Request, id: int | None = None):
    """
    Главная страница сайта.
    Возвращает шаблон index.html с передачей запроса в контекст.
    Параметр id необязателен и служит примером параметра пути.
    """
    return templates.TemplateResponse(
        request, "index.html"
    )

# Запуск основного приложения через сервер Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# Аргументы:
    # main:app — путь к главному приложению (название файла и переменная app)
    # host="127.0.0.1" — адрес прослушивания
    # port=8000 — номер порта
    # reload=True — автоматический перезапуск сервера при изменении файлов