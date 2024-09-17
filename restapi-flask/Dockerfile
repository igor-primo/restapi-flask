FROM python:3.9.19-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY application application
COPY wsgi.py config.py ./
EXPOSE 5000
CMD ["python", "wsgi.py"]