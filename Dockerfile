FROM python:3.8.7-slim-buster
ENV PYTHONUNBUFFERED=1
EXPOSE 7038

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt ./
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
COPY . ./

ENTRYPOINT [ "python" ]
CMD ["manage.py 0.0.0.0:7038"]