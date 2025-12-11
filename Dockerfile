FROM python:3.10-slim

ENV FLASK_CONTEXT=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/sysacad/.local/bin
# Creamos un usuario no-root por seguridad y establecemos el directorio de trabajo
RUN useradd --create-home --home-dir /home/sysacad sysacad
# Actualizamos apt, instalamos solo las herramientas de runtime necesarias,
# y limpiamos la caché en la misma capa para reducir el tamaño de la imagen.
# No necesitamos 'build-essential' o 'libpq-dev' porque 'psycopg2-binary' ya viene precompilado.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    htop \
    iputils-ping \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /home/sysacad
USER sysacad

EXPOSE 5000

# Usamos Gunicorn como un servidor WSGI de producción para manejar alta concurrencia.
# --bind 0.0.0.0:5000: Escucha en todas las interfaces de red dentro del contenedor.
# --workers 4: Inicia 4 procesos para manejar peticiones en paralelo. Un buen punto de partida es (2 * CPU cores) + 1.
# app:app: Le dice a Gunicorn que busque el objeto 'app' dentro del módulo 'app.py'.

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
