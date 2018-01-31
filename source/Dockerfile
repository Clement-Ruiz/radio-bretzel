FROM debian:stretch-slim

RUN apt-get update -y && apt-get install -y \
  liquidsoap \
  liquidsoap-plugin-all

COPY fail.mp3 /fail.mp3

WORKDIR /audio/test
COPY audio-test/ .

WORKDIR /scripts
COPY scripts/dummy.liq dummy.liq
COPY scripts/test.liq test.liq

RUN chown -R liquidsoap:liquidsoap /audio && \
   chown -R liquidsoap:liquidsoap /scripts && \
   find /audio -type d -exec chmod 500 {} \; && \
   find /audio -type f -exec chmod 400 {} \; && \
   find /scripts -type d -exec chmod 500 {} \; && \
   find /scripts -type f -exec chmod 400 {} \; && \
   chown liquidsoap:liquidsoap /fail.mp3 && \
   chmod 400 /fail.mp3

VOLUME /audio /scripts

ENV API_HOST="api.radiobretzel"
ENV SOURCE_ID="00000000-0000-0000-0000-000000000000"
ENV PATH = "/usr/bin/liquidsoap"

USER liquidsoap
WORKDIR /scripts

ENTRYPOINT ["/usr/bin/liquidsoap"]
CMD ["./test.liq"]
