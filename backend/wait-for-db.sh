#!/bin/bash
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for MySQL at $host"

until mysql -h "$host" -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e 'SHOW DATABASES;' > /dev/null 2>&1; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 5
done

>&2 echo "MySQL is up - executing command"
exec $cmd
