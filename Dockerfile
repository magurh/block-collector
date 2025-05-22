# Stage 1: Build Backend
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder
ADD . /block-collector
WORKDIR /block-collector
RUN uv sync --frozen

# Stage 2: Final Image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY --from=backend-builder /block-collector/.venv ./.venv
COPY --from=backend-builder /block-collector/src ./src
COPY --from=backend-builder /block-collector/pyproject.toml .
COPY --from=backend-builder /block-collector/README.md .

CMD ["uv", "run", "start-collection"]