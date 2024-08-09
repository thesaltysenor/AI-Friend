# Use an official Python runtime as a base image with CUDA support
FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04

# Set the working directory in the container to /app
WORKDIR /app

# Avoid interactive dialogues from apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Set the PYTHONPATH to include the /app directory
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Install system dependencies including MySQL client and development libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    mysql-client \
    libmysqlclient-dev \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential

# Add the deadsnakes PPA for newer Python versions
RUN add-apt-repository ppa:deadsnakes/ppa

# Install Python 3.10 and other necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    libffi-dev \
    libssl-dev \
    tzdata

# Update alternatives to prioritize Python 3.10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install the latest pip using get-pip.py
ADD https://bootstrap.pypa.io/get-pip.py /get-pip.py
RUN python3.10 /get-pip.py && \
    rm /get-pip.py

# Set the timezone (e.g., "Etc/UTC")
RUN echo "Etc/UTC" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Set environment variables for MySQL
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# Upgrade pip and install wheel
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -v

# Update this line to use cuda11.8 instead of cu118
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu120

# Install NLTK and download the required resources
RUN pip install nltk && \
    python -m nltk.downloader vader_lexicon && \
    python -m nltk.downloader stopwords && \
    python -m nltk.downloader punkt && \
    python -m nltk.downloader wordnet

# Copy the wait-for-db.sh script
COPY backend/wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Copy the backend directory contents into the container at /app
COPY backend/ /app/

# Copy the .env file into the container at /app
COPY .env /app/.env

# Clear Python's cache
RUN find /app -name '*.pyc' -delete || true && find /app -name '__pycache__' -delete || true

# List contents for debugging
RUN ls -R /app

# Expose port 8000 for the application
EXPOSE 8000

# Run the wait script and the application with uvicorn
CMD ["sh", "-c", "/app/wait-for-db.sh ai-friend-db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]