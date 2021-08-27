FROM tiangolo/uvicorn-gunicorn:python3.8-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Copy backend project folder
COPY ./backend/ ./backend/

# Copy alembic migrations
COPY ./.migrations/ ./.migrations/
COPY ./alembic.ini .

# Copy Scripts
COPY ./prestart.sh .

# Upgrade PIP
RUN pip install pip --upgrade

# Install pipenv
RUN pip install pipenv
COPY Pipfile .
COPY ./Pipfile.lock .
RUN pipenv install --deploy --system

RUN useradd admin && chown -R admin /app
USER admin

#COPY ./requirements.txt .
#RUN pip install -r requirements.txt --default-timeout=100 future

# Development Mode with Live Reload
ENTRYPOINT ["/start-reload.sh"]