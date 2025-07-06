ARG PYTHON_IMAGE=python:3.12.3

FROM ${PYTHON_IMAGE}

WORKDIR /app

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./cmd ./cmd
COPY ./config ./config
COPY ./alembic.ini  ./
COPY ./pyproject.toml ./
COPY ./poetry.lock*  ./

EXPOSE 80

ARG VENV_PATH_ARG="/opt/venv"
ENV VENV_PATH=$VENV_PATH_ARG

RUN python -m venv "$VENV_PATH"
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

CMD ["bash", "cmd/start/dev.sh"]