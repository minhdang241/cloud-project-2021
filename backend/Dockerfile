FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV ENV_CONFIG=""

EXPOSE 8000

CMD ["bash", "entrypoint.sh"]

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip3 install sentence-transformers

COPY . .