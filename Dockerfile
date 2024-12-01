FROM alpine:3.10

RUN apk add python3-dev \ 
    && pip3 install --upgrade pip

WORKDIR /app

COPY /src/* /app/
COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

EXPOSE 7000

CMD ["python3", "node.py"]