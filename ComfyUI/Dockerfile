FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/comfyanonymous/ComfyUI.git

WORKDIR /app/ComfyUI

RUN pip install -r requirements.txt

EXPOSE 8188

CMD ["python", "main.py", "--listen"]