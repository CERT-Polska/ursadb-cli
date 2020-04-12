FROM python:3.6

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app
RUN pip3 install .

ENTRYPOINT ["ursaclient"]
