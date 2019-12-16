FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libatlas-dev \
        wget \
        git \
        curl \
        nginx \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
    /opt/conda/bin/conda install conda-build conda-forge

ENV PATH=/opt/conda/bin:${PATH}

RUN git clone https://github.com/joshprewer/spleeter.git
RUN cd spleeter && ls && conda create -n spleeter -f requirements.txt
RUN conda clean -ya

ENV PATH /opt/conda/envs/spleeter/bin:$PATH
ENV USER spleeter

WORKDIR /spleeter

CMD source activate spleeter
CMD source ~/.bashrc

RUN conda update -y conda && \
    conda install -c flask gevent gunicorn && \
        rm -rf /root/.cache

# Python won’t try to write .pyc or .pyo files on the import of source modules
# Force stdin, stdout and stderr to be totally unbuffered. Good for logging
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY api /opt/program
WORKDIR /opt/program
RUN chmod 755 serve