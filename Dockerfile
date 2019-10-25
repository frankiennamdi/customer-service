FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app

ADD . /app
RUN python -m pip install pip==9.0.1 && \
    pip install pipenv && \
    pipenv install --dev --system --deploy --ignore-pipfile

EXPOSE 9090

ENTRYPOINT [ "python",  "manage.py"]