# cloudsql-connector-python

Python connector for Google Cloud SQL. This allows connection to a MySQL database in Google Cloud SQL without using cloud_sql_proxy.

Postgres is not currently supported.

# Usage

This can be used in place of the standard [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/).
Specify the instance identifier string as the "host" parameter.

    from cloudsql import (connection)

    con = connection.MySQLConnection(user='username', password='password', host='project:region:db_instance', database='database_name')
