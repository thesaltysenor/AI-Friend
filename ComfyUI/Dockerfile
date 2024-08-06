FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/comfyanonymous/ComfyUI.git

WORKDIR /app/ComfyUI

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8188

CMD ["python3", "main.py", "--listen"]