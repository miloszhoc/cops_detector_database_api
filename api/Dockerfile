FROM python:3.12
WORKDIR /workspace
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt
COPY . /workspace/cops_db_api
CMD ["uvicorn", "cops_db_api.cops_api:app", "--host", "0.0.0.0", "--port", "8003"]
