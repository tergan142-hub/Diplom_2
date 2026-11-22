# Diplom_2

# Stellar Burgers — API автотесты

Автотесты для API веб-приложения [Stellar Burgers](https://stellarburgers.education-services.ru/) — сервиса по сборке и заказу бургеров.

Тесты написаны на Python с использованием `pytest` и `requests`, покрывают эндпоинты создания пользователя, авторизации и создания заказа. Отчёты формируются в Allure.

## Стек

- **Python 3.10+**
- **pytest** — фреймворк для тестов
- **requests** — HTTP-клиент для работы с API
- **allure-pytest** — отчёты
- **Faker** / `uuid` — генерация уникальных тестовых данных

## Структура проекта
.
├── api/
│ └── api_client.py # Методы для работы с эндпоинтами
├── helpers/
│ └── data_generator.py # Генерация email, пароля, имени
├── tests/
│ ├── test_create_user.py # Тесты создания пользователя
│ ├── test_login_user.py # Тесты логина
│ └── test_create_order.py # Тесты создания заказа
├── conftest.py # Фикстуры (клиент, пользователь, токен)
├── constants.py # BASE_URL и ID ингредиентов
├── requirements.txt # Зависимости
└── README.md


## Установка

1. Клонируйте репозиторий:

   git clone <URL_РЕПОЗИТОРИЯ>
   cd <ИМЯ_ПАПКИ>

Создайте и активируйте виртуальное окружение:

python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Установите зависимости:

pip install -r requirements.txt

Установите Allure Commandline и добавьте его в PATH (нужно только для просмотра отчётов).

Запуск тестов

Все тесты:
pytest

С генерацией данных для Allure-отчёта:
pytest --alluredir=allure-results

С очисткой старых результатов перед прогоном:
pytest --alluredir=allure-results --clean-alluredir

Только один файл:
pytest tests/test_create_order.py -v

Просмотр Allure-отчёта

После прогона с --alluredir=allure-results:
allure serve allure-results
Откроется браузер с интерактивным отчётом: иерархия Epic → Feature → Story, шаги каждого API-запроса, статистика по severity.

Что проверяют тесты
Создание пользователя (test_create_user.py)
создание уникального пользователя — 200, success: true, есть accessToken;

создание пользователя, который уже зарегистрирован — 403, "User already exists";

создание пользователя без одного из обязательных полей (email, password, name) — 403, "Email, password and name are required fields".

Логин пользователя (test_login_user.py)
вход под существующим пользователем — 200, success: true, есть accessToken;

вход с неверным логином или паролем — 401, "email or password are incorrect".

Создание заказа (test_create_order.py)
создание заказа с авторизацией и ингредиентами — 200, success: true, есть name и order.number;

создание заказа без авторизации — фактическое поведение стенда;

создание заказа без ингредиентов — 400, "Ingredient ids must be provided";

создание заказа с неверным хешем ингредиента — 500.

Особенности реализации
ApiClient — класс-обёртка над requests.Session, инкапсулирует все запросы к API. Аналог Page Object, но для API.

Уникальные данные — email генерируется через uuid, поэтому тесты не зависят друг от друга и могут запускаться в любом порядке.

Фикстуры — unique_user создаёт пользователя, auth_token логинится и возвращает токен. Тесты создания заказа используют их, чтобы не дублировать подготовку.

Параметризация — проверка незаполненных полей и неверных учётных данных реализована через @pytest.mark.parametrize, без if/elif/else.

Allure — на тестах @allure.epic, @allure.feature, @allure.story, @allure.title, @allure.severity; на методах ApiClient — @allure.step, чтобы в отчёте были видны шаги запросов.

Тестовые данные
Email генерируется уникально для каждого теста (uuid).

Пароль — фиксированный password123.

Имя — фиксированное TestUser.

ID ингредиентов — реальные _id из ответа GET /api/ingredients, хранятся в constants.py.