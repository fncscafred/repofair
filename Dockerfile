FROM python:3.11-slim

LABEL maintainer="Francisca Frederick <fnbella97@gmail.com>"
LABEL description="repofair — FAIR Repository Audit Tool"
LABEL version="1.0.0"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-m", "repofair.cli"]
CMD ["."]
