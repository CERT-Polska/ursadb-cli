FROM python:3.6

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/python3", "ursaclient.py"]
