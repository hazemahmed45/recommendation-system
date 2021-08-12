From python:3.7.0

WORKDIR /app

COPY . .
RUN apt update 
RUN pip install --upgrade pip
RUN pip install -r require.txt







EXPOSE 8080

ENTRYPOINT ["python","./run.py"]