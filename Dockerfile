# 
FROM python:3.10

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./src /app/src

ENV PYTHONPATH "${PYTHONPATH}:/app/src"
ENV PYTHONUNBUFFERED 1

# 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]