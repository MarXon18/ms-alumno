FROM python:3.10-slim

ENV FLASK_CONTEXT=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/sysacad/.local/bin

# 1. Creamos usuario no-root
RUN useradd --create-home --home-dir /home/sysacad sysacad

# 2. Dependencias del Sistema
# DEFENSA: "Eliminamos curl y htop para reducir superficie de ataque.
# Solo dejamos lo mínimo para que Python corra."
WORKDIR /home/sysacad

# 3. Instalación de Dependencias Python (Aprovechando Caché)
# Copiamos solo el requirements primero. Si no cambias dependencias,
# Docker se salta este paso y usa la memoria caché (Build más rápido).
COPY --chown=sysacad:sysacad requirements.txt .

# Instalamos uv y luego las dependencias con uv.
# --no-cache: Para que la imagen pese menos.
# Instala uv y luego usa uv para instalar las dependencias del proyecto de forma eficiente.
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -r requirements.txt

USER sysacad


# 4. Copia del Código Fuente
# Copiamos el resto de los archivos con los permisos correctos.
COPY --chown=sysacad:sysacad . .

EXPOSE 5000

# 5. Ejecución
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]


