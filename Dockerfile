# Base image of Python
FROM python:3.9-slim

# Label of metadatos (opcional)
LABEL maintainer="Label Test Dokerfile. Created by ..."

# Definition of env variables
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

# Set thw work directory in the docker
WORKDIR $APP_HOME

# Copy requirements file in the container
COPY requirements.txt .

# Install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in the container
COPY . .

# Expose the port to listen
EXPOSE 5000

# Define new user to run the aplication
RUN useradd -m myappuser
USER myappuser

# Command to run when the container inicialize
CMD ["python", "app.py"]
