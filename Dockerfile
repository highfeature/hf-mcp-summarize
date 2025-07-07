# Base Image and System Dependencies
# TODO: see to replace all "alpine" image with image of open minded provider
FROM python:3.12-alpine
# Install system dependencies required by uv
RUN apk add --no-cache curl git

# Install uv safely
RUN curl -LsSf -o /tmp/install_uv.sh https://astral.sh/uv/install.sh && \
    sh /tmp/install_uv.sh && \
    rm /tmp/install_uv.sh

# Set PATH to include uv
ENV PATH="/root/.local/bin:$PATH"

# Create app directory and set permissions
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project --no-dev --python-preference=only-system

# Copy the rest of the project files
COPY . .

# Run the FastAPI application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

