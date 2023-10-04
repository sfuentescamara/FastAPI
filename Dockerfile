# Base image of Python
FROM python:3.9-slim

# Label of metadatos (opcional)
LABEL maintainer="Label Test Dokerfile. Created by ..."

# Definition of env variables
ENV PYTHONUNBUFFERED False
ENV APP_HOME /app

# Set thw work directory in the docker
WORKDIR $APP_HOME

# Copy requirements file in the container
COPY requirements.txt .

# Instalamos virtualenv y creamos un entorno virtual llamado "venv"
RUN pip install virtualenv && \
    virtualenv venv

# Activamos el entorno virtual
ENV PATH="/app/venv/bin:$PATH"

# Install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in the container
# COPY . .
COPY app_deployment.py .

# Expose the port to listen
EXPOSE 8080
EXPOSE 8088

# Define new user to run the aplication
RUN useradd -m myappuser
RUN chown -R myappuser:myappuser /app
USER myappuser

# Command to run when the container inicialize
CMD ["python", "app_deployment.py"]

# build the image
# docker build -t flask_app .../flask_api/
# run the container
# docker run -d -p 8080:80 nombre_imagen
# run container to develop
# docker run -v flusk_api:/develop -d -p 80:8080 -p 88:8088 flask_api