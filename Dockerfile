FROM python:3.14-slim@sha256:7a500125bc50693f2214e842a621440a1b1b9cbb2188f74ab045d29ed2ea5856

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY gitlab_cicd_python_wrapper/ gitlab_cicd_python_wrapper/
RUN poetry install --only=main --no-interaction --no-ansi

ENTRYPOINT ["gitlab-cicd-validate"]
