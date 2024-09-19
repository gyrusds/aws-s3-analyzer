# Establecer la imagen base
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

RUN pip install --upgrade pip

# Copiar los archivos de dependencias
COPY pyproject.toml poetry.lock /app/

# Instalar las dependencias con Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copiar el código fuente
COPY . /app

# Establecer el comando de inicio
CMD ["poetry", "run", "python", "src/main.py"]
