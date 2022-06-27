FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN addgroup --system flask \
    && adduser --system --ingroup flask flask
RUN chown -R flask:flask /app
USER flask
CMD [ "python3", "app.py"]