FROM nikolaik/python-nodejs
LABEL maintainer ="watchit"

ENV PROJECT_ROOT /data/watchit/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

# Get dependencies
RUN npm i
RUN pip3 install ipfshttpclient
RUN pip3 install py-cid
RUN pip3 install validators
RUN pip3 install -r requeriments.txt
COPY . $PROJECT_ROOT
