# Тестовое задание в компанию "Простые решения"

## Docker
Docker ожидает на вход следующие переменные окружения:
```
# Для Postgres
DB_NAME
DB_USER
DB_PASS

# Для Django
DJANGO_SECRET_KEY

# Используется как затычка во время сборки.
# В production ссылка создается на postgres
# с указанными выше параметрами
DATABASE_URL

# Для Stripe
STRIPE_PUBLISHABLE_API_KEY
STRIPE_SECRET_API_KEY
```

Для удобства рекомендуется вынести их в файл `.env`.

Пример содержания `.env` файла:
```
DJANGO_SECRET_KEY=django-insecure-m_6s*qcs4gs_-i$9kl8t2yw!d1h7yavie_e3@bg5q8cr@=8)%f
DB_NAME=testdb
DB_USER=testuser
DB_PASS=testpassword
DATABASE_URL=sqlite://./db.sqlite3
STRIPE_PUBLISHABLE_API_KEY=pk_test_TYooMQauvdEDq54NiTphI7jx
STRIPE_SECRET_API_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc
```

Для сборки и запуска можно воспользоваться следующими командами:
```bash
docker compose --env-file .env -f docker-compose.yml build
docker compose --env-file .env -f docker-compose.yml up -d
```

Миграция БД не включена в процесс сборки, поэтому необходимо дополнительно осуществить миграцию либо через запущенный контейнер:
```bash
docker ps

# Вместо container_id использовать идентификатор контейнера,
# который узнали с помощью команды выше
docker exec -it container_id bash
python manage.py migrate
```

, либо установить зависимости вручную из системы и так же выполнить команду:
```bash
python manage.py migrate
```

Для использования Django Admin панели необходимо таким же образом (из работающего контейнера) вызвать следующую команду и создать суперпользователя:
```bash
python manage.py createsuperuser
```

## Пояснения к реализации
- В задании указано реализовать 2 API метода, но второй метод должен возвращать HTML-страницу, поэтому API запрос заменен на HTML-шаблон (в результате чего некоторые запросы используют API, в то время как другие - формы)
- Для заказа с несколькими пунктами для простоты использован session (дабы избежать лишнюю логику авторизации)
- При оформлении покупки создается запись в БД и обычно для таких действий используется метод POST, однако для соблюдения задания используется метод GET
