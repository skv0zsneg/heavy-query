FROM python

COPY . /src

WORKDIR /src

RUN apt update && apt install -y libpq-dev
RUN pip install -r requirements.txt

CMD [ "python3", "server.py" ]