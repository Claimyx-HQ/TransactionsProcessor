FROM public.ecr.aws/lambda/python:3.10

# Install Tesseract and its dependencies
RUN yum update -y && \
    yum install -y amazon-linux-extras && \
    amazon-linux-extras enable epel && \
    yum install -y epel-release && \
    yum install -y tesseract tesseract-langpack-eng && \
    yum clean all && \
    rm -rf /var/cache/yum

COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME /usr/local/openjdk-8
# RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

# Set the working directory in the container
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock ./
COPY pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

# Copy the rest of your application code to the container
COPY . ./

# Copy the .env file to the container
#COPY .env ./

# Set the CMD to specify the Lambda handler
CMD ["transactions_processor.main.lambda_handler"]
