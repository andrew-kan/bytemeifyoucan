FROM python:3.8
RUN curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.7.tgz
RUN tar -zxvf mongodb-linux-x86_64-3.6.7.tgz
RUN mv mongodb-linux-x86_64-3.6.7/ /mongodb/
RUN mkdir -p /mongodb/db && mkdir -p /mongodb/log
COPY ./src/ /backend
RUN pip install -r /backend/requirements.txt
WORKDIR /backend/src
CMD ["bash", "start.sh"]
EXPOSE 8080