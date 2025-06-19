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

SHELL ["/bin/bash", "-c"]

RUN source "$VENV_PATH/bin/activate" && pip install poetry
RUN source "$VENV_PATH/bin/activate" && poetry config virtualenvs.create false
RUN source "$VENV_PATH/bin/activate" && poetry install --no-root

CMD ["bash", "cmd/start-dev.sh"]