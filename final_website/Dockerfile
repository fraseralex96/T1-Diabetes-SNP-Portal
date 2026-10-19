FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# R + build tooling (rpy2 needs R and headers to build its cffi bindings)
RUN apt-get update && apt-get install -y --no-install-recommends \
        r-base \
        r-base-dev \
        build-essential \
        gcc \
        libffi-dev \
        libblas-dev \
        liblapack-dev \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
        libuv1-dev \
        libfontconfig1-dev \
        libfreetype6-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        libpng-dev \
        libjpeg-dev \
        libtiff-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# R package used by manfunction.R (add any others it loads)
# Tries CRAN first, falls back to GitHub, and fails the build if still missing
# (install.packages alone only warns, which is why the failure was silent)
RUN Rscript -e 'options(repos=c(CRAN="https://cloud.r-project.org"), Ncpus=4); \
    install.packages("manhattanly"); \
    if (!requireNamespace("manhattanly", quietly=TRUE)) { \
      install.packages("remotes"); \
      remotes::install_github("sahirbhatnagar/manhattanly", upgrade="never"); \
    }; \
    if (!requireNamespace("manhattanly", quietly=TRUE)) quit(status=1)'

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 5000

# main.py calls init_db() and app.run() under __main__, so run it directly
CMD ["python", "main.py"]