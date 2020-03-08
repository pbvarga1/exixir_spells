FROM python:3.7

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -U pip
RUN pip install virtualenv
RUN virtualenv venv
RUN venv/bin/pip-3.7 install --no-cache-dir -e spells_db/

FROM elixir:latest

COPY --from=0 /app /app

ENV PYTHONPATH=/app/venv/bin/python3.7

RUN ls

WORKDIR /app
RUN $PYTHONPATH -v

WORKDIR /app/spells

RUN ls
RUN ls assets/

RUN apt-get update && apt-get -y install inotify-tools nodejs npm
RUN npm install npm@latest -g

RUN ls

WORKDIR /app/spells/assets

RUN ls

RUN npm install
WORKDIR /app/spells

# Install hex
RUN mix local.hex --force
RUN mix local.rebar --force

RUN mix deps.get --force

RUN mix do compile

CMD ["mix", "phx.server"]
