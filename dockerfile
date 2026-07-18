FROM python:3.14.5-slim

# Cài uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy file dependency trước để tận dụng cache
COPY pyproject.toml uv.lock ./

# Cài package
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Chạy project
CMD ["uv", "run", "python", "main.py"]