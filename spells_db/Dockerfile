FROM python:3.7

RUN mkdir -p /app/spells_db
WORKDIR /app/spells_db

COPY . /app/spells_db

RUN pip install --no-cache-dir -e .

CMD ["python", "run_app.py"]
