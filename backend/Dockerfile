FROM python:rc-alpine

WORKDIR /usr/src/radiobretzel
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
   pip install -r requirements.txt

VOLUME /usr/src/radiobretzel /var/run/docker.sock
EXPOSE 5000

ENV RADIO_BRETZEL_ENV development

CMD ["./run.py"]
