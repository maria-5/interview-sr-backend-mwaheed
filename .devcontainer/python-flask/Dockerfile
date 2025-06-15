FROM mcr.microsoft.com/devcontainers/base:ubuntu

ENV PYTHONUNBUFFERED 1

# Install wget, gnupg2, and lsb-release (needed to add PostgreSQL repo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg2 lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Add PostgreSQL official repo for version 17
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Update and install postgresql-client-17 and libpq-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-17 libpq-dev \
    && rm -rf /var/lib/apt/lists/*