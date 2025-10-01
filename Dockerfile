# CI/CD Example - Multi-stage Docker Build
FROM python:3.11-slim as base

# Metadata
LABEL maintainer="MLOps Team"
LABEL description="CI/CD Example API"
LABEL version="1.0.0"

# System dependencies ve security updates
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Non-root user oluştur (security best practice)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Working directory
WORKDIR /app

# Python dependencies (caching için önce requirements)
COPY config/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Application code
COPY src/ ./src/
COPY config/ ./config/

# Permissions
RUN chown -R appuser:appuser /app
USER appuser

# Environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Port expose
EXPOSE ${PORT}

# Command
CMD ["python", "src/app.py"]

# Development stage (multi-stage build)
FROM base as development

# Switch back to root for dev tools installation
USER root

# Development dependencies
COPY config/requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Development tools
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy tests for development
COPY tests/ ./tests/

# Switch back to appuser
USER appuser

# Override command for development
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

# Testing stage
FROM development as testing

# Run tests
RUN python -m pytest tests/ -v --cov=src/

# Production stage (final optimized stage)
FROM base as production

# Production-only optimizations
ENV FLASK_ENV=production
ENV PYTHONOPTIMIZE=1

# Final command
CMD ["python", "src/app.py"]