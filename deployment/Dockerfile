FROM python:3.12-slim-bookworm AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY ./pyproject.toml ./uv.lock* /tmp/

# Install Python dependencies into the system
RUN cd /tmp && \
    uv pip install --system --no-cache-dir .


# ----------- Runtime Stage ----------- #
FROM python:3.12-slim-bookworm

LABEL maintainer="Daniel Pantoja"

# Set working directory
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code
COPY ./src /app


# Copy and set up entrypoint
COPY ./deployment/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose application port
EXPOSE 8000

# Execute entry script
ENTRYPOINT [ "./entrypoint.sh" ]
