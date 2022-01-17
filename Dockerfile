FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

# Install pip requirements
ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

ADD . /app

# runs as appuser
RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

CMD ["flask", "run"]
