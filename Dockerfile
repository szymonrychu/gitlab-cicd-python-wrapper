FROM python:3.14-slim@sha256:3989a23fd2c28a34c7be819e488b958a10601d421ac25bea1e7a5d757365e2d5

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY gitlab_cicd_python_wrapper/ gitlab_cicd_python_wrapper/
RUN poetry install --only=main --no-interaction --no-ansi

ENTRYPOINT ["gitlab-cicd-validate"]
