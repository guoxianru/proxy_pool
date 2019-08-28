FROM python:3.6
ENV DEBIAN_FRONTEND noninteractive
ENV TZ Asia/Shanghai
WORKDIR /srv/proxy_pool
ADD . /srv/proxy_pool
EXPOSE 5010
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD [ "python3", "Run/main.py" ]