FROM python:3.6
ENV DEBIAN_FRONTEND noninteractive
ENV TZ Asia/Shanghai
ADD . /srv/proxy_pool
WORKDIR /srv/proxy_pool
EXPOSE 5010

RUN mkdir /root/.pip
COPY ./pip.conf /root/.pip/pip.conf
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "Run/main.py" ]