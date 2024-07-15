# Build stage
FROM amazonlinux:2 as builder

# Install build dependencies
RUN yum update -y && \
    yum groupinstall -y "Development Tools" && \
    yum install -y \
        wget \
        tar \
        gzip \
        libpng-devel \
        libjpeg-devel \
        libtiff-devel \
        zlib-devel \
        libwebp-devel \
        gcc-c++ \
        autoconf \
        automake \
        libtool \
        pkgconfig \
        make

# Build Leptonica
RUN wget http://www.leptonica.org/source/leptonica-1.82.0.tar.gz && \
    tar -xzvf leptonica-1.82.0.tar.gz && \
    cd leptonica-1.82.0 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf leptonica-1.82.0*

# Build Tesseract
RUN wget https://github.com/tesseract-ocr/tesseract/archive/4.1.1.tar.gz && \
    tar -xzvf 4.1.1.tar.gz && \
    cd tesseract-4.1.1 && \
    ./autogen.sh && \
    PKG_CONFIG_PATH=/usr/local/lib/pkgconfig LIBLEPT_HEADERSDIR=/usr/local/include ./configure --prefix=/usr/local --disable-openmp && \
    make && \
    make install && \
    cd .. && \
    rm -rf 4.1.1.tar.gz tesseract-4.1.1

# Download English language data
RUN mkdir -p /usr/local/share/tessdata && \
    wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata -O /usr/local/share/tessdata/eng.traineddata

# Final stage
FROM public.ecr.aws/lambda/python:3.10

# Copy Tesseract and its dependencies from builder
COPY --from=builder /usr/local/bin/tesseract /usr/local/bin/
COPY --from=builder /usr/local/lib/libtesseract.so* /usr/local/lib/
COPY --from=builder /usr/local/lib/liblept.so* /usr/local/lib/
COPY --from=builder /usr/local/share/tessdata/eng.traineddata /usr/local/share/tessdata/

# Install runtime dependencies
RUN yum update -y && \
    yum install -y \
        libpng \
        libjpeg \
        libtiff \
        libwebp \
        ghostscript && \
    yum clean all && \
    rm -rf /var/cache/yum

# Set Tesseract environment variables
ENV TESSDATA_PREFIX=/usr/local/share/tessdata
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Verify Tesseract installation
RUN echo "Verifying Tesseract installation:" && \
    tesseract --version

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
