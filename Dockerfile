FROM python:3.14-slim@sha256:b877e50bd90de10af8d82c57a022fc2e0dc731c5320d762a27986facfc3355c1

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY gitlab_cicd_python_wrapper/ gitlab_cicd_python_wrapper/
RUN poetry install --only=main --no-interaction --no-ansi

ENTRYPOINT ["gitlab-cicd-validate"]
