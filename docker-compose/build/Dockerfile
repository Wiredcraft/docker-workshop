FROM python:alpine

RUN pip install redis tornado

COPY server.py /

EXPOSE 8080

CMD python server.py 
