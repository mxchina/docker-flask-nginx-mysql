FROM python:2.7-alpine
ADD  . /app/
WORKDIR /app/
RUN  apk update && apk add gcc libc-dev linux-headers
RUN  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT ["uwsgi","uwsgi_config.ini"]
