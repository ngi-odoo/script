#!/bin/bash

# Get the list of PostgreSQL databases
db_list=$(psql -t -c "SELECT datname FROM pg_database")

# Loop through the list of databases
for db in $db_list
do
    # Update the value if the key is "database.expiration_date" in the current database
    psql -d $db -c "UPDATE ir_config_parameter SET value = CURRENT_DATE + INTERVAL '1 year' WHERE key = 'database.expiration_date';"
    echo "Update performed in database $db."
done