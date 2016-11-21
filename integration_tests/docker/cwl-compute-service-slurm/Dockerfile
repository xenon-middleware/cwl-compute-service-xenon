# Build with:
#
# docker build -t nlesc/cwl-compute-service-slurm .
#
# Run with:
#
# docker run -d --name=cwl-compute-service-slurm nlesc/cwl-compute-service-slurm
#
# Test with:
#
# ssh xenon@<ip of xenon-slurm container>

FROM phusion/baseimage:0.9.17
MAINTAINER Lourens Veen "l.veen@esciencecenter.nl"

RUN rm -f /etc/service/sshd/down
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Upgrade OS
RUN apt-get update && apt-get upgrade -y -o Dpkg::Options::="--force-confold" && \
  apt-get install -y mailutils slurm-llnl python3 git python-pip && \
  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
  pip install virtualenv

# Create a test user
RUN /usr/sbin/useradd -p $(openssl passwd javagat) -d /home/xenon -m --shell /bin/bash xenon
WORKDIR /home/xenon
RUN mkdir in out && chown -R xenon in out

COPY munge.key /etc/munge/munge.key
COPY service /etc/service
# Key was generated with openssl genrsa -out slurm.key 1024 && openssl rsa -in slurm.key -pubout -out slurm.cert
COPY etc /etc/slurm-llnl

RUN mkdir /var/run/munge && \
  mkdir -p /var/spool/slurmctld/state /var/spool/slurmd.node-0 /var/spool/slurmd.node-1 && \
  chmod 600 /etc/munge/munge.key && \
  chown root.root /var/lib/munge /etc/munge && \
  touch /var/spool/slurmctld/accounting.txt /var/spool/slurmctld/job_completions.txt /var/spool/slurmctld/state/recv_state && \
  chown slurm -R /var/spool/slurmctld /etc/slurm-llnl/slurm.key

USER root
CMD ["/sbin/my_init"]
