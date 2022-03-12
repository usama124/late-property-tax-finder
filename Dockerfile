FROM python:3.8

RUN apt-get update
RUN apt-get install -y
RUN apt install wget -y


RUN apt-get update
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


WORKDIR /app
COPY src /app/.
#RUN pip install -r requirements.txt

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
RUN cd /app
WORKDIR /app
RUN pwd
RUN ls
#ENTRYPOINT ["python3", "main.py"]