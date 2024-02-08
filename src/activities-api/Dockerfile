# syntax=docker/dockerfile:1

FROM python:3.11-slim as builder

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install -q --no-cache-dir poetry poetry-plugin-export
RUN poetry check --lock && poetry export -o requirements.txt

COPY . /app/src/activities-api

RUN poetry build

FROM python:3.11-slim as requirements

COPY --from=builder /app/requirements.txt /tmp/
RUN pip install -q -r /tmp/requirements.txt && rm /tmp/requirements.txt

FROM requirements AS runner

COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm -rf /tmp/*.whl

WORKDIR /usr/local/lib/python3.11/site-packages/activities-api/

CMD ["python", "app.py"]
