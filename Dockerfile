FROM python:3
LABEL maintainer="Mofesola Babalola <me@mofesola.com>"
WORKDIR /usr/src/
COPY . .
RUN ls -al
RUN pip install -r app/requirements.txt

CMD [ "python", "app/main.py" ]
