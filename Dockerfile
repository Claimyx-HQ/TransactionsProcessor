# Use the official Python image as the base image
FROM python:3.10
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME /usr/local/openjdk-8

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1


# Set the working directory in the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry shell
RUN poetry install

# Copy the rest of your application code to the container
COPY . /app
COPY .env /app/.env

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn
CMD ["uvicorn", "transactions_process_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
