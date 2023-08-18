FROM python:3.7-slim

WORKDIR /app/

COPY requirements.txt /app/
RUN pip install -r ./requirements.txt

COPY app.py /app/
COPY final_model_gender.pkl /app/
COPY final_model_age_group.pkl /app/
COPY test_data_gender.pkl /app/
COPY test_data_age_group.pkl /app/
COPY templates/index.html /app/templates/index.html
COPY static/css/style.css /app/static/css/style.css

ENTRYPOINT ["python"]

CMD ["app.py"]

EXPOSE 5000