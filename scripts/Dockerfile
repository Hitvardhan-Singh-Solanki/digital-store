FROM python:3.9

WORKDIR /scripts

COPY ./requirements.txt /scripts/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /scripts

ENV PYTHONPATH=/scripts

CMD ["python", "simulate_webhook.py"]