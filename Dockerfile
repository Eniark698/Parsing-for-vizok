FROM python:3.11.6-bullseye
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y git curl wget firefox-esr 
#RUN apt-get install -y lsb-release && lsb_release -a && sleep 5
RUN apt-get install -y iputils-ping


RUN sh -c 'curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc'
RUN sh -c 'curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list'
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

WORKDIR /app

COPY ./requirements-311.txt /app/
RUN pip install -r requirements-311.txt
RUN python -m playwright install 

COPY . /app/
CMD ["/bin/sh", "-c", "sleep 10000000000"]