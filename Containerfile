# Poetry-friendly containerfile, via https://stackoverflow.com/a/57886655
# !! This runs the Flask dev server, with everything that implies !!

FROM python:3.10-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONBUFFERED=1

WORKDIR /app


FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl


FROM base as final
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}" \
    FLASK_APP=labelstore:app
CMD ["flask", "run", "--host=0.0.0.0"]
