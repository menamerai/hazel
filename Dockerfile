FROM python:3.12-bullseye

RUN pip install poetry==1.8.3

COPY . .

RUN poetry config virtualenvs.create false

RUN poetry install

ENTRYPOINT [ "poetry", "run", "python", "-m", "hazel.main" ]