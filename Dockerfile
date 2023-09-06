FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED 1

#install and use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app
COPY . /app

EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["./django.sh"]
