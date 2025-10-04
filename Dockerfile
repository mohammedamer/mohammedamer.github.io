FROM ubuntu:24.04

LABEL MAINTAINER="Mohammed E. Amer <mohammed.amer@fujitsu.com>"

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
RUN apt update && apt install -y ffmpeg software-properties-common

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml uv.lock .python-version /app/

WORKDIR /app/
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

RUN apt-add-repository -y ppa:rael-gc/rvm
RUN apt-get update
RUN apt-get install -y openssl

COPY .ruby-version .
RUN gpg --keyserver keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
RUN \curl -L https://get.rvm.io | bash -s stable
RUN /bin/bash -l -c "rvm requirements"
RUN /bin/bash -l -c "rvm install $(cat .ruby-version)"

RUN /bin/bash -l -c 'gem install jekyll bundler'

RUN apt install -y git

COPY Gemfile Gemfile.lock beautiful-jekyll-theme.gemspec .

RUN /bin/bash -l -c 'bundle install'

WORKDIR /app/src/