FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y cron nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN ln -snf /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo "Asia/Tehran" > /etc/timezone

RUN echo "30 07 * * * (/usr/local/bin/python /app/domain/task.py && /usr/local/bin/python /app/server/task.py && /usr/local/bin/python /app/certificate/task.py) >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron && \
    chmod 0644 /etc/cron.d/mycron && \
    crontab /etc/cron.d/mycron && \
    touch /var/log/cron.log

COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /var/www/html && cp -r template/* /var/www/html/

EXPOSE 8000
CMD ["bash", "/app/deploy.sh"]