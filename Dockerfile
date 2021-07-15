FROM python:3.9.6-alpine3.14
WORKDIR /usr/src/deals_project
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt /usr/src/deals_project
RUN pip install --upgrade pip
RUN pip install -r /usr/src/deals_project/requirements.txt
COPY ./env.dev .
#COPY ./entrypoint.sh .
COPY . .
#ENTRYPOINT ["/usr/src/deals_project/entrypoint.sh"]
