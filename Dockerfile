FROM python:3.8.5-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip uninstall uvloop -y & python -m spacy download en_core_web_trf
COPY . .
EXPOSE 9015
CMD [ "python3","-m","src.main" ]