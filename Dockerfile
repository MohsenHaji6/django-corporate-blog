FROM node:22 AS frontend

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm ci

COPY . .

RUN npm run build


FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

RUN pip install uv

COPY uv.lock .
COPY pyproject.toml .

RUN uv sync

EXPOSE 8000

COPY . .

RUN rm /code/static/src/input.css

COPY --from=frontend /app/static/css/output.css /code/static/css/output.css

ENTRYPOINT [ "/code/entrypoint.sh" ]

CMD [ "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1" ]