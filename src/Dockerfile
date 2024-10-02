FROM python:3.9-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY setup.py .
RUN python setup.py install

COPY . .

EXPOSE 4000

CMD ["python", "api_gateway"]
