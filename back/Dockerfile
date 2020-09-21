FROM python:3.7-alpine3.11
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip
WORKDIR server
COPY . .
RUN pip install -r requirements.txt \
  && apk del build-dependencies
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
