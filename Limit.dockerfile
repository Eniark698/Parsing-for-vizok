FROM python:3.11.6-bullseye
ENV DEBIAN_FRONTEND noninteractive

# Disable IPv6
RUN echo "net.ipv6.conf.all.disable_ipv6=1" >> /etc/sysctl.conf && \
    echo "net.ipv6.conf.default.disable_ipv6=1" >> /etc/sysctl.conf && \
   echo "net.ipv6.conf.lo.disable_ipv6=1" >> /etc/sysctl.conf && \
   echo "net.ipv6.conf.tun0.disable_ipv6=1" >> /etc/sysctl.conf



#RUN apt-get install -y git curl wget
RUN sh -c 'curl https://packages.microsoft.com/keys/microsoft.asc |  tee /etc/apt/trusted.gpg.d/microsoft.asc'
RUN sh -c 'curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list'
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
unixodbc-dev \
firefox-esr \
iputils-ping \
iproute2 \
traceroute \
nano \
vim \
openvpn \
ca-certificates \
unzip \
sqlite3


WORKDIR /app


COPY ./temp_cred.txt /app/
RUN chmod 777 temp_cred.txt



COPY ./requirements-311.txt /app/
RUN pip install -r requirements-311.txt && python -m playwright install firefox


COPY ./startup_limit.sh /app/startup_limit.sh
RUN chmod 777 startup_limit.sh
COPY ./.env /app/.env
COPY ./google_shop/ /app/google_shop/

#CMD ["/bin/sh", "-c", "python ./google_shop/main.py"]
CMD ["/bin/sh", "-c", "sleep infinity"]
#CMD ["/bin/sh", "-c", "./startup_limit.sh"]