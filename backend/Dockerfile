FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel
RUN pip install numpy Cython
RUN pip install --no-build-isolation --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]