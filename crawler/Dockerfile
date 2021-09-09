FROM python:3.7

WORKDIR /app

RUN pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install psycopg2

RUN pip3 install python-dotenv

COPY . .

CMD ["scrapy", "crawl", "indeed_job"]
