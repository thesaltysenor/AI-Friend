# Use an official Python runtime as a base image with CUDA support
FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04

# Set the working directory in the container to /app
WORKDIR /app

# Set all environment variables at once
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH="/app:${PYTHONPATH}" \
    MYSQLCLIENT_CFLAGS="-I/usr/include/mysql" \
    MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# Copy all necessary files at once
COPY requirements.txt backend/wait-for-db.sh backend/ .env ./

# Add get-pip.py using ADD instruction
ADD https://bootstrap.pypa.io/get-pip.py /tmp/get-pip.py

# Install system dependencies, Python, set up the environment, and install Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libffi-dev \
    libmysqlclient-dev \
    libssl-dev \
    mysql-client \
    pkg-config \
    software-properties-common \
    tzdata \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && python3.10 /tmp/get-pip.py \
    && rm /tmp/get-pip.py \
    && echo "Etc/UTC" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt -v \
    && pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu120 \
    && pip install nltk \
    && python -m nltk.downloader vader_lexicon stopwords punkt wordnet \
    && chmod +x /app/wait-for-db.sh \
    && find /app -name '*.pyc' -delete || true \
    && find /app -name '__pycache__' -delete || true \
    && ls -R /app \
    && rm -rf /var/lib/apt/lists/*

# Expose port 8000 for the application
EXPOSE 8000

# Run the wait script and the application with uvicorn
CMD ["sh", "-c", "/app/wait-for-db.sh ai-friend-db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]