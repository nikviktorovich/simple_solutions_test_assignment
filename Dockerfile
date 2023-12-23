FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY}

ARG DATABASE_URL
ENV DATABASE_URL ${DATABASE_URL}

ARG STRIPE_PUBLISHABLE_API_KEY
ENV STRIPE_PUBLISHABLE_API_KEY ${STRIPE_PUBLISHABLE_API_KEY}

ARG STRIPE_SECRET_API_KEY
ENV STRIPE_SECRET_API_KEY ${STRIPE_SECRET_API_KEY}

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
RUN python manage.py collectstatic --noinput

CMD ["python", "-m", "gunicorn", "django_project.wsgi", "--bind=0.0.0.0:8000"]
