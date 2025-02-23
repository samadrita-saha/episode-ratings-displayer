FROM python:3.11-slim as builder

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y g++ gcc make

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends chromium chromium-driver

RUN apt autoclean && rm -rf /var/lib/apt/lists/*

COPY . .

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["flask", "run", "--host", "0.0.0.0"]