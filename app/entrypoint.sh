# entrypoint.sh

# Получаем имя пользователя, пароль, хост бд и имя бд из .env-файла
# Перед запуском проверяем, что существуют все перечисленные переменные и названия совпадают с представленными в скрипте

#Проверяем, что бд существует и не пуста
if PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c 'select 1;' > /dev/null; then
    echo "Database already exists, skipping migration creation."
else
    echo "Database does not exist or is empty. Creating initial migration."
    alembic revision --autogenerate -m "init"
fi

# Запускаем миграции
alembic upgrade head

# Запускаем приложение
uvicorn app.main:app --host 0.0.0.0 --port 8888
