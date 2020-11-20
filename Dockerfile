FROM python:3.7-slim

WORKDIR /service
COPY ./service/requirements.txt .
RUN pip install -r requirements.txt

COPY ./service /service

EXPOSE 5001/tcp
ENTRYPOINT ["python"]
CMD ["compression-service.py"]
