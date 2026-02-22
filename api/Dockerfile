FROM python:3.12
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt
COPY . .
CMD ["uvicorn", "cops_api:app", "--host", "0.0.0.0", "--port", "8003"]
