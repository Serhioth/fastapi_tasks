# fastapi_tasks

_API-сервис для CRM-систем_

**Описание:**

Пример простого API для работы с задачами пользователей.

Включает в себя:

- Систему аутентификации пользователей через JWT-токены.
- Полноценный CRUD для пользователей и их задач.
- Фильтрацию задач пользователей по их названию и дате создания.


**Стек:**

- Python
- Bash
- FastAPI
- FastAPI Users
- SQLAlchemy
- PostreSQL
- Docker
- Docker-compose

**Для тестового запуска на локальной машине:**

1. Установите Docker и Docker-compose на свой компьютер (инструкции [здесь](https://docs.docker.com/engine/install/))
2. Клонируйте данный репозиторий
3. Создайте свой файл переменных среды (.env) согласно представленному в проекте .env.example
4. Запустите docker-compose (инструкции [здесь](https://docs.docker.com/get-started/08_using_compose/#run-the-application-stack))
Пример:
```bash
docker-compose up --build -d
```
6. Документация к запущенному проекту будет находиться по адресу:
   - **Swagger:** _http://localhost:8888/dosc_
   -  **ReDoc:** _http://localhost:8888/redoc_

