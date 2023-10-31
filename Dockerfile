FROM python:3.11.6-bullseye
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get install -y git curl wget
RUN sh -c 'curl https://packages.microsoft.com/keys/microsoft.asc |  tee /etc/apt/trusted.gpg.d/microsoft.asc'
RUN sh -c 'curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list'
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev firefox-esr iputils-ping iproute2 traceroute nano vim
#RUN apt-get install -y lsb-release && lsb_release -a && sleep 5




WORKDIR /app

COPY ./requirements-311.txt /app/
RUN pip install -r requirements-311.txt
RUN python -m playwright install 

COPY ./.env /app/.env
COPY ./google_shop/ /app/google_shop/

#CMD ["/bin/sh", "-c", "python ./google_shop/main.py"]
CMD [/bin/sh", "-c", "sleep 100000000"]