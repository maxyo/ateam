FROM amd64/python:3
#FROM python:3-alpine3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

CMD [ "python", "ateam.py", "--output=output.json", "--matrix=matrix.json", "--hbcount=5", "--algo=PATH_MOST_CONSTRAINED_ARC", "--metaalgo=TABU_SEARCH"]