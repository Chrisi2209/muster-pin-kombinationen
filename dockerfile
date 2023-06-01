FROM python:3

WORKDIR /muster-pin-kombination
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python" "src/main.py"]
