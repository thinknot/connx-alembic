FROM python:3.11-slim as base

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./templates /app/templates
COPY ./*.py /app/
COPY ./swagger.yml /app/

# ==================
FROM base as debug

RUN pip install debugpy

CMD python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py

# ==================
FROM base as prod

CMD python app.py
