FROM public.ecr.aws/lambda/python:3.10

# Install Tesseract and its dependencies
RUN yum update -y && \
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum install -y \
        git \
        libtool \
        gcc-c++ \
        zlib \
        zlib-devel \
        libjpeg \
        libjpeg-devel \
        libwebp \
        libwebp-devel \
        libtiff \
        libtiff-devel \
        libpng \
        libpng-devel \
        tesseract \
        tesseract-langpack-eng && \
    yum clean all && \
    rm -rf /var/cache/yum

# Copy necessary libraries
RUN cp /usr/lib64/libjpeg.so.62 /usr/local/lib/ && \
    cp /usr/lib64/libwebp.so.4 /usr/local/lib/ && \
    cp /usr/lib64/libtiff.so.5 /usr/local/lib/ && \
    cp /usr/lib64/libpng15.so.15 /usr/local/lib/

# Set Tesseract environment variables
ENV TESSDATA_PREFIX=/usr/share/tesseract/tessdata
ENV LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH

# Verify Tesseract installation
RUN echo "Verifying Tesseract installation:" && \
    if [ -f /usr/bin/tesseract ]; then \
        echo "Tesseract binary found at /usr/bin/tesseract"; \
        /usr/bin/tesseract --version; \
    else \
        echo "Tesseract binary not found"; \
        exit 1; \
    fi

# List relevant libraries
RUN echo "Listing relevant libraries:" && \
    ls -l /usr/lib64/libtesseract* /usr/lib64/liblept* /usr/lib64/libgif* \
          /usr/lib64/libwebp* /usr/lib64/libtiff* /usr/lib64/libpng* \
          /usr/lib64/libjpeg*

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
