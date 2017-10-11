FROM python:3.6.3

EXPOSE 5000

ENV APP_DIR /usr/src/pyiso_api

RUN mkdir $APP_DIR

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN pip install -r requirements.txt && \
    chmod -R ug+rw $APP_DIR

ENTRYPOINT ["gunicorn"]

CMD ["app:app", "-w", "4", "-b", "0.0.0.0:5000", "--worker-class", "meinheld.gmeinheld.MeinheldWorker", "--error-logfile", "-", "--access-logfile", "-"]
