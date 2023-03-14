FROM python:3.9-slim-buster

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./main.py /code
COPY ./fun /code/fun
COPY ./bd /code/bd
COPY ./util /code/util

ARG root_path

ENV ROOT_PATH=${root_path}

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 80 --root-path=$ROOT_PATH"]

