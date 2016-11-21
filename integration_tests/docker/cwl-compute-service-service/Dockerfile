FROM alpine:3.4
MAINTAINER Lourens Veen <l.veen@esciencecenter.nl>

# install requirements
RUN apk add --no-cache openjdk7-jre python python-dev py-pip git build-base curl && \
  pip install virtualenv

RUN adduser -D cwl-compute-service

USER cwl-compute-service
RUN git clone https://github.com/NLeSC/cwl-compute-service-xenon.git \
  /home/cwl-compute-service/cwl-compute-service-xenon

WORKDIR /home/cwl-compute-service/cwl-compute-service-xenon

RUN virtualenv env \
  && . env/bin/activate \
  && pip install -U pip \
  && make install

USER root
COPY start.sh /start.sh
COPY config.ini /home/cwl-compute-service/cwl-compute-service/config.ini
RUN chown -R cwl-compute-service:cwl-compute-service /home/cwl-compute-service

USER cwl-compute-service
EXPOSE 3596
ENTRYPOINT ["/bin/sh"]
CMD ["/start.sh"]
