FROM alpine:3.9

RUN apk add --no-cache --update \
        python3 \
        uwsgi \
    	uwsgi-python3

ARG user=app
ARG workdir=/home/${user}
ARG requirements=requirements.freeze.txt

RUN addgroup -S ${user} && adduser -G ${user} -S ${user}

USER ${user}

WORKDIR ${workdir}

# only copy the requirements.freeze.txt file so that the
# next run command to install python packages is not executed unless
# the requirements.freeze.txt file changes
COPY --chown=app:app ${requirements} ${workdir}

RUN python3 -m venv venv-app \
    && source venv-app/bin/activate \
    && python3 -m pip install --upgrade pip setuptools \
    && pip3 install --no-cache-dir --requirement ${requirements}

COPY --chown=app:app . ${workdir}

CMD ["uwsgi", "--yaml", "uwsgi.yaml"]

EXPOSE 8080
