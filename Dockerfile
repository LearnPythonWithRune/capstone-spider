FROM python:3.10-bullseye

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /src
COPY . /src

WORKDIR /src

CMD ["python", "spider.py", "--host", "host.docker.internal", "--city", "Copenhagen"]