# Base image
FROM python:3.11-slim

# Install Python dependencies
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Copy application requirements
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY src/ src/

# Set the working directory
WORKDIR /

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN pip install . --no-deps --no-cache-dir

# Entry point for the evaluation script
ENTRYPOINT ["python", "-u", "src/mlops_solo_project/evaluate.py"]