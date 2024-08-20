# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * In the virtualenv: Update pip setuputils and wheel to support building new packages
FROM debian:12-slim AS build
RUN apt update \
    && apt install \
        --no-install-suggests \
        --no-install-recommends \
        --yes \
        python3-venv \
        gcc \
        libpython3-dev \
    && python3 -m venv venv/ \
    && /venv/bin/pip install --upgrade pip setuptools wheel

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-env
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install \
        --disable-pip-version-check \
        -r /requirements.txt

# Copy the virtualenv to the distroless image
FROM gcr.io/distroless/python3-debian12
COPY --from=build-env /venv /venv
COPY . /store-service
WORKDIR /store-service
EXPOSE 5000
ENTRYPOINT [ "/venv/bin/flask", "--app", "server:app", "run", "-h", "0.0.0.0" ]