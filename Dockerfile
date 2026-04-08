FROM python:3.11-slim@sha256:b1b81d67b8df73bf6067191790c233ef9e598b863fc1ccf447956138ca466d99

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY gitlab_cicd_python_wrapper/ gitlab_cicd_python_wrapper/
RUN poetry install --only=main --no-interaction --no-ansi

ENTRYPOINT ["gitlab-cicd-validate"]
