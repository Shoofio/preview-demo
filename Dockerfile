FROM python:3.12-slim

WORKDIR /app

# Build-time arguments (injected by CI)
ARG COMMIT_SHA=unknown
ARG PR_NUMBER=N/A
ARG BRANCH_NAME=unknown
ARG BUILD_TIME=unknown
ARG IMAGE_TAG=unknown

# Set as environment variables for runtime
ENV COMMIT_SHA=${COMMIT_SHA}
ENV PR_NUMBER=${PR_NUMBER}
ENV BRANCH_NAME=${BRANCH_NAME}
ENV BUILD_TIME=${BUILD_TIME}
ENV IMAGE_TAG=${IMAGE_TAG}

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .

# Run with gunicorn for production
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "main:app"]

