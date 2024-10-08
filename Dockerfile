FROM python:3.11

# set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y python3-opencv

# copy files
COPY src/mystroke_api /app/src/mystroke_api
COPY pyproject.toml /app/
COPY "MyStroke_model" "/app/MyStroke_model"
COPY README.md /app/
COPY .python-version /app/

# install dependencies
RUN pip install python-multipart
RUN pip3 install .

# run server
CMD ["uvicorn", "src.mystroke_api.main:app", "--host", "0.0.0.0", "--port", "5000"]

#CMD ["pip3", "list"]

# bind port
EXPOSE 5000