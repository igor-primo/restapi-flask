FROM python:3.9.19-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY wsgi.py .
COPY config.py .
COPY application .
EXPOSE 5000
CMD ["python", "wsgi.py"]