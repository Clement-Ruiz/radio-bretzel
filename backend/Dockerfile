FROM python:rc-alpine

WORKDIR /usr/src/radiobretzel
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
   pip install -r requirements.txt

VOLUME /usr/src/radiobretzel /var/run/docker.sock
EXPOSE 5000

# ENTRYPOINT ["/usr/bin/python"]
CMD ["python", "run.py"]
