FROM python:3.9

WORKDIR /opt/

COPY requirements.txt .

COPY app.py .

RUN pip3 install -r /opt/requirements.txt

EXPOSE 8080

CMD ["gunicorn", "app:app", "--timeout=6000", "--preload", "--workers=1", "--threads=4", "--bind=0.0.0.0:8080"]
