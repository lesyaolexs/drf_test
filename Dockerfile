FROM python:3.8-slim-buster

ARG USERNAME=app-user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /drf_test
WORKDIR /drf_test


RUN pip install poetry virtualenv
RUN poetry config virtualenvs.create false

COPY  ./poetry.lock .
COPY ./pyproject.toml  .

RUN poetry install

COPY ./app app/
COPY ./drf_test/  drf_test/
COPY ./manage.py .

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]