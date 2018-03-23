FROM python:2.7
ADD  . /app/
WORKDIR /app/
RUN  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT ["uwsgi","uwsgi_config.ini"]
