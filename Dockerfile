FROM python:3.11-slim

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY gitlab_cicd_python_wrapper/ gitlab_cicd_python_wrapper/
RUN poetry install --only=main --no-interaction --no-ansi

ENTRYPOINT ["gitlab-cicd-validate"]
