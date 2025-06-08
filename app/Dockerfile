FROM python:3-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip3 install -r requirements.txt

#COPY . /app

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]