FROM python:3.9

WORKDIR /scripts

COPY ./requirements.txt /scripts/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /scripts

ENV PYTHONPATH=/scripts

CMD ["uvicorn", "payment_intent_server:app", "--host", "0.0.0.0", "--port", "8001"]