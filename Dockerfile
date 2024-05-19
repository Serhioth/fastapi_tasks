# Используем лёгкий базовый образ
FROM python:3.11-slim

# Устагнавливаем рабочукю директорию

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости (без кэширования, чтобы контейнер весил меньше)
RUN pip install -U pip && \
    pip install -r requirements.txt --no-cache-dir
# Устанавливаем клиент для работы с БД
RUN apt-get update && apt-get install -y postgresql-client
# Копируем приложение в контейнер
COPY . .

# Пробрасываем порт 8888 из контейнера во внешнюю среду
EXPOSE 8888