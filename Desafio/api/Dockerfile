FROM python:3.7

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ARG DEBUG='False'
ARG ENV='production'

ENV DEBUG=${DEBUG}
ENV ENV=${ENV}

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]