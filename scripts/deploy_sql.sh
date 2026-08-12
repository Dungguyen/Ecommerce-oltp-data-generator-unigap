#!/bin/bash

CONTAINER=ecommerce_postgres
USER=nguyendung
DB=ecommerce_oltp

echo ""
echo "Deploy SQL Objects"
echo ""

for folder in sql/views sql/functions sql/procedures
do
    if [ -d "$folder" ]; then

        for file in $(find "$folder" -name "*.sql" | sort)
        do
            echo "Deploying $(basename "$file")"

            docker exec -i $CONTAINER \
            psql -U $USER -d $DB < "$file"

        done

    fi
done

echo ""
echo "Deploy Finished"