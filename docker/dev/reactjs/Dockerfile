FROM ubuntu:16.04

RUN apt-get update -qq && apt-get install -y build-essential git curl libfontconfig

RUN apt-get install nodejs-legacy -y

RUN apt-get install npm -y

RUN apt-get install -y ruby-dev

RUN gem install sass -v 3.2.19

WORKDIR /code

ADD . /code

RUN npm link gulp

RUN npm cache clean -f
RUN npm install -g n
RUN n stable

RUN npm install

RUN npm install --save-dev json-loader

RUN npm install -g webpack@1.13.1

CMD ["webpack", "--progress", "--watch", "--colors"]
