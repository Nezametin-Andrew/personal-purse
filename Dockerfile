FROM python:3.8

WORKDIR /src

COPY requirements.txt /src
COPY entrypoint.sh /src

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . /src

ENTRYPOINT ["/src/entrypoint.sh"]