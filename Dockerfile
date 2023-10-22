FROM python:3.9
ENV DB_URL=
ENV WITHIN_DOCKER_ENV=1
WORKDIR /code
RUN  pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
COPY ./pyproject.toml /code/pyproject.toml
COPY ./setup.cfg /code/setup.cfg
COPY ./setup.py /code/setup.py
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install -e .
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
