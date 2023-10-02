## Flask api
Primero de todo crear una estructura para la aplicación flask con python. La distribución de archivos seguirá la siguiente forma:

```
flask_api/
    api/
        __init__.py
        model/
            __init__.py
        route/
            __init__.py
        schema/
            __init__.py
        service/
            __init__.py
    test/
        test.py
    app.py
    config.py
    requirements.txt
```
Una vez se tiene la aplicación flask se usará docker para crear la imagen y kubernetes para levartar el servicio.

## Configuración Dockerfile
Se añade un archivo Docker en el directorio raiz (flask_api/) con la siguiente configuración:

Dockerfile
```
# Usa una imagen base oficial de Python
FROM python:3.8

# Etiqueta para metadatos (opcional)
LABEL maintainer="Tu Nombre <tu@email.com>"

# Establece un directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos (requirements.txt) al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación escucha
EXPOSE 8080

# Define un usuario no privilegiado para ejecutar la aplicación
RUN useradd -m myappuser
USER myappuser

# Comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["python", "app.py"]

```

Para evitar copiar contenido inecesario en el docker se puede usar el archivo .dockerignore y añadir:

```
Dockerfile
README.md
*.pyc
*.pyo
*.pyd
__pycache__
.pytest_cache
```
Una vez creado el docker file se puede crear la imagen con:

```docker build -t <nombre_imagen> .../flask_api/```

y correr el contenerdor con:

```docker run -d -p 8080:80 <nombre_imagen>```

## Configuración Kubernetes 
Una vez creada la imagen se puede utilizar kubernetes para desplegar la imagen docker en un clúster.

** INFO.
Para crear la configuración de Kubernetes vamos a distinguir los recursos tipo 'Deployment' y 'service'.

- Deployment: se utiliza para definir cómo se crean y gestionan los pods de una aplicación en un clúster.
    ```
    apiVersion: apps/v1
    kind: Deployment
    metadata:
        name: nombre-del-deployment
    spec:
        replicas: 3
        selector:
            matchLabels:
            app: nombre-de-la-app
        template:
            metadata:
            labels:
                app: nombre-de-la-app
            spec:
                containers:
                    name: nombre-del-contenedor
                    image: nombre-de-la-imagen
                    ports:
                        containerPort: 8080
    ```
- Service: se utiliza para definir cómo se accederá a los pods (generalmente mediante un servicio de red).
    ```
    apiVersion: v1
    kind: Service
    metadata:
        name: nombre-del-servicio
    spec:
        selector:
            app: nombre-de-la-app
        ports:
            protocol: TCP
            port: 80
            targetPort: 8080
        type: ClusterIP
    ```

Una vez creado creado el archivo de configuración se puede ejecutar de la siguiente manera

```kubectl apply -f deployment.yaml```

