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

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]