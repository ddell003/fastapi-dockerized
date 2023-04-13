# Server build stage
FROM python:3.9-alpine as builder

WORKDIR /app

# needed to install psycopg2
# we won't need if we decide to use SqlAlchemy
RUN apk add --no-cache --virtual .build-deps \
   postgresql-dev \
   gcc \
   python3-dev \
   musl-dev

COPY ./requirements.txt requirements.txt

# pip install here will download and save dependencies into
# /usr/local/lib/python3.9/site-packages/
# we'll copy these over into the final image
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-alpine

ENV DB_NAME=${DB_NAME:-api}
ENV DB_HOST=${DB_HOST:-localhost}
ENV DB_PORT=${DB_PORT:-5432}
ENV DB_USERNAME=${DB_NAME:-api_user}
ENV DB_PASSWORD=${DB_NAME:-password}
ENV API_AUTHORIZED_DOMAINS=${API_AUTHORIZED_DOMAINS:-*}
ENV API_AUTHORIZED_WHITELIST=${API_AUTHORIZED_WHITELIST:-*}
ENV POSTGRES_SCHEMA=${POSTGRES_SCHEMA}
ENV ALLOWED_ORIGIN=${ALLOWED_ORIGIN:-"http://localhost:3000"}
ENV INIT_DATA_PATH=${INIT_DATA_PATH:-/opt/data}

RUN pip install uvicorn
RUN apk add --no-cache libpq

# copy the python dependencies
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/alembic /usr/local/bin/alembic

EXPOSE 5000

WORKDIR /opt

COPY ./api ./api
COPY ./static ./static
COPY ./data ./data
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

### Going to move the alembic and data-loading scripts to another pattern.
### We shouldn't be running this every time the container starts.
# ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
