FROM postgres:10.5
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres
ADD 10-db-init.sql /docker-entrypoint-initdb.d/
#ADD 11-db-characters.pgsql /docker-entrypoint-initdb.d/
EXPOSE 5432
