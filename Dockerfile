FROM python:3.11-slim

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-interaction --no-ansi

COPY gitlab_cicd_python_wrapper/ gitlab_cicd_python_wrapper/

ENTRYPOINT ["gitlab-cicd-validate"]
