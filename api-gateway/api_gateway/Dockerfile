FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./

COPY cred.json .

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "app:app", "--timeout=6000", "--preload", "--workers=1", "--threads=4", "--bind=0.0.0.0:8080"]
