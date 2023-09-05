FROM python:3.11-bullseye as python-base

FROM python-base as poetry

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN poetry export -f requirements.txt --dev --without-hashes -o dev_requirements.txt

FROM python-base as api-base

LABEL description="Medications API"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ENABLE_DOCUMENTATION
ARG DEBUG
ARG BACKEND_PORT
ARG FRONTEND_APP_PORT

ENV ENABLE_DOCUMENTATION=$ENABLE_DOCUMENTATION
ENV DEBUG=$DEBUG
ENV BACKEND_PORT=$BACKEND_PORT
ENV FRONTEND_APP_PORT=$FRONTEND_APP_PORT

LABEL ENABLE_DOCUMENTATION=$ENABLE_DOCUMENTATION
LABEL DEBUG=$DEBUG
LABEL BACKEND_PORT=$BACKEND_PORT
LABEL FRONTEND_APP_PORT=$FRONTEND_APP_PORT

ENV APP /workspace

RUN apt-get update

RUN mkdir -p $APP
WORKDIR $APP

COPY --from=poetry requirements.txt .
RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY . .

FROM api-base as test-env

COPY --from=poetry dev_requirements.txt .
RUN pip install --no-cache-dir --no-deps -r dev_requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8005", "src.main:app"]
