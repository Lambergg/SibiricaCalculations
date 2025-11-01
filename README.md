MVP-проект для компании "Сибирица" по расчёту кол-ва и стоимости товара-мульчи.
Использованные технологии: FastAPI, Pydantic, HTML, CSS, Git, Docker.
Приложение развёрнуто на облачном сервере при помощи Docker-контейнера.
Приложение решает задачу: Облегчение работы менеджеров по продажам прирасчёте товара.
Функции для расчёта кэшированны при помощи встроенной библиотеки functools и lru_cache.
Адрес приложения: 45.12.231.210

Предупреждение

Если у вас Python 3.9 или ниже, замените <тип1> | <тип2> на Union[<тип1>, <тип2>]

Создание репозитория

git init
git remote add origin git@github.com:<никнейм>/<названиеРепозитория>.git
.... add gitignore

git add .

git commit -m "..."

git branch -M main

git push -u origin main

Подготовка сервера

git
sudo apt-get update

sudo apt-get install git

docker

Можно воспользоваться инструкцией: https://docs.docker.com/engine/install/ubuntu/ или скопировать код ниже

sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

Запуск приложения

Создание образа (коробки) с приложением

docker build . --tag fastapi_app

Запуск образа в контейнере с пробросом портов для доступа к контейнеру из интернета

docker run -p 80:8000 fastapi_app