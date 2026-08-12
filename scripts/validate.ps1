$container="ecommerce_postgres"

docker exec $container `
psql `
-U nguyendung `
-d ecommerce_oltp `
-c "\dv"

docker exec $container `
psql `
-U nguyendung `
-d ecommerce_oltp `
-c "\df"