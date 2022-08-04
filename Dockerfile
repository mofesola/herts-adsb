FROM python:3.9.9
LABEL maintainer="Mofesola Babalola <me@mofesola.com>"
WORKDIR /usr/src/
COPY . .
RUN pip install -r app/requirements.txt

CMD [ "python", "app/main.py" ]
