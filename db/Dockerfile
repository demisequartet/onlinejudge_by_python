FROM postgres:11-alpine
ENV LANG="ja_JP.UTF-8" LANGUAGE="ja_JP:ja" LC_ALL="ja_JP.UTF-8"
EXPOSE 5432
ADD ["all.sql", "/docker-entrypoint-initdb.d/"]
ADD ["submit.sql", "/docker-entrypoint-initdb.d/"]