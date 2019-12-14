FROM ubuntu:16.04

# Install python and other scikit-learn runtime dependencies
# Dependency list from http://scikit-learn.org/stable/developers/advanced_installation.html#installing-build-dependencies
RUN apt-get update && \
    apt-get -y install build-essential libatlas-dev wget curl nginx jq libatlas3-base libgcc-5-dev  libgcc-5-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -bfp /miniconda3 && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH=/miniconda3/bin:${PATH}

RUN conda update -y conda && \
    conda install -c conda-forge musdb spleeter==1.4.5 flask gevent gunicorn && \
        rm -rf /root/.cache

# Python won’t try to write .pyc or .pyo files on the import of source modules
# Force stdin, stdout and stderr to be totally unbuffered. Good for logging
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY api /opt/program
WORKDIR /opt/program