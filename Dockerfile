FROM python:3.10-slim


ARG APP_PATH=/app
ARG APP_USER=appuser

ADD ./requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

RUN groupadd --system ${APP_USER} && \
    useradd --no-create-home -u 1000 -r -g ${APP_USER} ${APP_USER}

COPY --chown=${APP_USER}:${APP_USER} service/ ${APP_PATH}

EXPOSE 8000

WORKDIR ${APP_PATH}

USER ${APP_USER}:${APP_USER}

CMD python3 manage.py collectstatic --noinput && \
		python3 manage.py migrate && \
		gunicorn --worker-class=gthread -b 0.0.0.0:8000 wsgi:application