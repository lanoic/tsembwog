FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend as a package folder
COPY . /app/backend

# Copy everything from backend context, incl. alembic.ini and alembic/
#COPY . /app

#COPY alembic.ini /app/alembic.ini
#COPY alembic /app/alembic

# Ensure Python can import the 'backend' package
ENV PYTHONPATH=/app

#CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh","-c","alembic -c /app/backend/alembic.ini upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]

#CMD ["sh","-c","alembic -c /app/alembic.ini upgrade head && uvicorn backend.main:app --host #0.0.0.0 --port 8000"]


