# Ecommerce OLTP Data Generator & Data Warehouse

A complete Data Engineering project that demonstrates how to generate e-commerce transactional data, store it in a PostgreSQL OLTP database, build a dimensional Data Warehouse, orchestrate the ETL process with Apache Airflow, and visualize business metrics using Microsoft Power BI.

The project follows this architecture:

```text
E-commerce Data Generator
        │
        ▼
┌─────────────────────┐
│   ecommerce_oltp    │
│   PostgreSQL 17     │
│                     │
│ orders              │
│ orders_item         │
│ customer            │
│ product             │
│ seller              │
│ brand               │
│ category            │
│ promotion           │
│ promotion_product   │
└──────────┬──────────┘
           │
           │ Airflow ETL
           │ PostgreSQL dblink
           ▼
┌─────────────────────┐
│    ecommerce_dw     │
│    PostgreSQL 17    │
│                     │
│ dim_date            │
│ dim_customer        │
│ dim_product         │
│ dim_seller          │
│ dim_brand           │
│ dim_category        │
│ fact_sales          │
└──────────┬──────────┘
           │
           │ PostgreSQL
           ▼
┌─────────────────────┐
│     Power BI        │
│                     │
│ KPI                 │
│ Revenue Analysis    │
│ Category Analysis   │
│ Sales Analysis      │
└─────────────────────┘
```

---

## 1. Project objectives

This project demonstrates an end-to-end Data Engineering workflow:

* Generate large-scale e-commerce transactional data.
* Store transactional data in PostgreSQL OLTP.
* Design a Star Schema Data Warehouse.
* Separate transactional and analytical workloads.
* Build an ETL pipeline with Apache Airflow.
* Load data from `ecommerce_oltp` into `ecommerce_dw`.
* Process data month by month to control memory and database resources.
* Validate source and destination data.
* Create analytical SQL views/functions.
* Connect PostgreSQL Data Warehouse to Power BI.
* Build dashboards for business analysis.

---

## 2. Technologies

| Technology            | Purpose                               |
| --------------------- | ------------------------------------- |
| Python                | Data generation and processing        |
| PostgreSQL 17         | OLTP and Data Warehouse               |
| Docker                | Containerization                      |
| Docker Compose        | Multi-container orchestration         |
| Apache Airflow 2.10.5 | ETL orchestration                     |
| PostgreSQL dblink     | Transfer/query data between databases |
| Power BI Desktop      | Data visualization                    |
| SQL                   | Data modeling, ETL and analytics      |
| Git/GitHub            | Version control                       |

---

## 3. Main components

The project contains three major services.

### 3.1 E-commerce Generator

Container:

```text
ecommerce_generator
```

This service generates transactional data and inserts it into PostgreSQL.

The generated data includes:

```text
customer
product
seller
brand
category
orders
orders_item
promotion
promotion_product
```

---

### 3.2 PostgreSQL

Container:

```text
ecommerce_postgres
```

PostgreSQL contains two main databases:

```text
ecommerce_oltp
ecommerce_dw
```

These are two separate PostgreSQL databases hosted by the same PostgreSQL server.

### OLTP

```text
ecommerce_oltp
```

Stores operational/transactional data.

### Data Warehouse

```text
ecommerce_dw
```

Stores transformed analytical data.

---

### 3.3 Apache Airflow

Containers:

```text
airflow_webserver
airflow_scheduler
```

Airflow orchestrates the ETL process.

The main DAG is:

```text
ecommerce_dw_etl
```

---

# 4. Database architecture

## 4.1 OLTP database

Database:

```text
ecommerce_oltp
```

Main tables:

```text
customer
product
seller
brand
category
orders
orders_item
promotion
promotion_product
```

The OLTP database is optimized for transactional operations.

For example:

```sql
SELECT COUNT(*)
FROM orders;
```

and:

```sql
SELECT COUNT(*)
FROM orders_item;
```

---

# 5. Data Warehouse architecture

Database:

```text
ecommerce_dw
```

Schema:

```text
dw
```

The Data Warehouse follows a Star Schema.

```text
                    dim_customer
                         │
                         │
                         ▼
dim_date ───────────► fact_sales ◄────────── dim_product
                         │
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         dim_seller   dim_brand  dim_category
```

---

## 5.1 Fact table

```text
dw.fact_sales
```

This is the central fact table.

Important columns include:

```text
date_key
customer_key
product_key
seller_key
brand_key
category_key

orders_id
orders_item_id

status
quantity
unit_price
subtotal
total_amount
```

`orders_item_id` is used as the business-level unique identifier for fact records.

---

## 5.2 Dimension tables

### Date

```text
dw.dim_date
```

Contains date-related attributes such as:

```text
date_key
full_date
year
quarter
month
week
day
```

### Customer

```text
dw.dim_customer
```

Contains:

```text
customer_key
customer_id
customer_name
gender
address
city
state
customer_created_at
```

### Product

```text
dw.dim_product
```

Contains product information such as:

```text
product_key
product_id
product_name
price
stock_quantity
rating
is_active
product_created_at
brand_id
category_id
```

### Seller

```text
dw.dim_seller
```

Contains:

```text
seller_key
seller_id
seller_name
seller_type
rating
country
join_date
```

### Brand

```text
dw.dim_brand
```

Contains brand information.

### Category

```text
dw.dim_category
```

Contains category information.

---

# 6. Why use two databases?

The project intentionally separates:

```text
ecommerce_oltp
```

and:

```text
ecommerce_dw
```

The OLTP database is responsible for operational transactions.

The Data Warehouse is responsible for analytical queries.

This separation prevents analytical workloads from directly affecting the transactional system.

For example:

```text
OLTP
    ↓
orders
orders_item
customer
product
    ↓
ETL
    ↓
Data Warehouse
    ↓
fact_sales + dimensions
    ↓
Power BI
```

---

# 7. Prerequisites

Before running the project, install:

### Docker Desktop

Make sure Docker is running:

```powershell
docker --version
```

```powershell
docker compose version
```

### Git

```powershell
git --version
```

### Power BI Desktop

Power BI is required for the final visualization stage.

### Optional: PostgreSQL client

`psql` can be installed locally for easier database access.

---

# 8. Clone the project

Clone the repository:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Enter the project:

```powershell
cd project3_DE_Unigap
```

---

# 9. Project structure

The project is organized around Docker, SQL and Airflow.

A typical structure is:

```text
project3_DE_Unigap/
│
├── docker-compose.yml
│
├── Dockerfile
│
├── pyproject.toml
│
├── dags/
│   └── ecommerce_dw_etl.py
│
├── sql/
│   ├── create_tables.sql
│   ├── views/
│   │   ├── vw_fact_sales.sql
│   │   ├── vw_products_sales.sql
│   │   ├── vw_sales_summary.sql
│   │   └── vw_seller_performance.sql
│   │
│   └── procedures/
│       ├── sp_load_fact_sales.sql
│       ├── sp_refresh_sales.sql
│       └── sp_update_order_total.sql
│
├── deploy_sql.ps1
├── validate.ps1
│
├── data/
│
├── logs/
│
└── README.md
```

The exact folder structure can vary depending on the current version of the project.

---

# 10. Start Docker

From the project directory:

```powershell
docker compose up -d --build
```

Check running containers:

```powershell
docker ps
```

You should see services similar to:

```text
airflow_scheduler
airflow_webserver
ecommerce_postgres
ecommerce_generator
```

Example:

```text
CONTAINER ID   IMAGE                    PORTS
xxxxxxxx       apache/airflow:2.10.5   8080/tcp
xxxxxxxx       apache/airflow:2.10.5   0.0.0.0:8080->8080/tcp
xxxxxxxx       postgres:17              0.0.0.0:5432->5432/tcp
xxxxxxxx       project3_de_unigap-app
```

---

# 11. Check PostgreSQL

Connect to PostgreSQL:

```powershell
docker exec -it ecommerce_postgres psql -U nguyendung -d postgres
```

List databases:

```sql
\l
```

You should have:

```text
airflow_db
ecommerce_dw
ecommerce_oltp
postgres
```

Exit:

```sql
\q
```

---

# 12. Check OLTP database

Connect:

```powershell
docker exec -it ecommerce_postgres psql -U nguyendung -d ecommerce_oltp
```

Check tables:

```sql
\dt
```

Check order data:

```sql
SELECT COUNT(*)
FROM orders;
```

Check order item data:

```sql
SELECT COUNT(*)
FROM orders_item;
```

Check product data:

```sql
SELECT COUNT(*)
FROM product;
```

Check the date range:

```sql
SELECT
    MIN(orders_date) AS min_date,
    MAX(orders_date) AS max_date
FROM orders;
```

---

# 13. Check Data Warehouse

Connect:

```powershell
docker exec -it ecommerce_postgres psql -U nguyendung -d ecommerce_dw
```

Check schemas:

```sql
\dn
```

Check DW tables:

```sql
\dt dw.*
```

You should see tables similar to:

```text
dim_brand
dim_category
dim_customer
dim_date
dim_product
dim_seller
fact_sales
```

---

# 14. Install PostgreSQL dblink

The ETL uses PostgreSQL `dblink` to query the OLTP database from the Data Warehouse.

Inside `ecommerce_dw`:

```sql
CREATE EXTENSION IF NOT EXISTS dblink;
```

Verify:

```sql
\dx
```

You should see:

```text
dblink
```

---

# 15. Test connection between OLTP and DW

From:

```text
ecommerce_dw
```

run:

```sql
SELECT *
FROM dblink(
    'host=host.docker.internal
     port=5432
     dbname=ecommerce_oltp
     user=nguyendung
     password=<POSTGRES_PASSWORD>
     options=''-c max_parallel_workers_per_gather=0''',
    $$
        SELECT
            current_database(),
            COUNT(*)
        FROM customer
    $$
) AS t(
    db_name TEXT,
    customer_count BIGINT
);
```

Expected result:

```text
db_name          | customer_count
-----------------+---------------
ecommerce_oltp   | ...
```

This confirms:

```text
ecommerce_dw
      │
      │ dblink
      ▼
ecommerce_oltp
```

is working.

> Do not commit database passwords to GitHub. Store credentials in environment variables or Airflow Connections.

---

# 16. Load dimension tables

Before loading the fact table, dimension tables must contain the corresponding source data.

The required dimensions are:

```text
dim_date
dim_customer
dim_product
dim_seller
dim_brand
dim_category
```

The number of rows in a dimension should be checked against the source database.

For example:

```sql
SELECT COUNT(*)
FROM dw.dim_product;
```

and:

```sql
SELECT COUNT(*)
FROM dw.dim_customer;
```

Source:

```sql
SELECT COUNT(*)
FROM product;
```

```sql
SELECT COUNT(*)
FROM customer;
```

---

# 17. Important dimension-table validation

Fact loading depends on successful dimension matching.

For example, every product in the OLTP should exist in:

```text
dw.dim_product
```

Every seller should exist in:

```text
dw.dim_seller
```

Every customer should exist in:

```text
dw.dim_customer
```

Otherwise the `JOIN` between the source data and dimensions can remove fact rows.

This was particularly important during development.

For example, if the source contains:

```text
5880 products
```

then the Data Warehouse should also contain:

```text
5880 products
```

before loading `fact_sales`.

---

# 18. Airflow

Airflow Web UI:

```text
http://localhost:8080
```

Open the Airflow interface and locate:

```text
ecommerce_dw_etl
```

The DAG performs:

```text
check_oltp
     │
     ▼
get_months
     │
     ▼
load_month[0]
load_month[1]
load_month[2]
load_month[3]
load_month[4]
     │
     ▼
validate_dw
```

The months are:

```text
January 2025
February 2025
March 2025
April 2025
May 2025
```

---

# 19. Why load month by month?

The OLTP dataset can be very large.

Trying to transfer all five months simultaneously can create:

* high memory consumption
* excessive PostgreSQL temporary files
* high CPU usage
* connection failures
* Docker resource exhaustion
* Airflow task failures

Therefore the ETL processes one month at a time.

Conceptually:

```text
January
   ↓
validate
   ↓
February
   ↓
validate
   ↓
March
   ↓
validate
   ↓
April
   ↓
validate
   ↓
May
   ↓
validate
```

This is much safer than processing all months concurrently.

---

# 20. Incremental loading

The fact table uses:

```sql
ON CONFLICT (orders_item_id)
DO NOTHING;
```

This makes the ETL idempotent for already-loaded fact records.

If January has already been successfully loaded, running the DAG again does not need to insert those same `orders_item_id` values again.

The ETL can therefore safely resume after a failure.

Example:

```text
January   → already loaded
February  → already loaded
March     → failed
April     → not started
May       → not started
```

The pipeline should be designed so completed periods are not unnecessarily reprocessed.

Before reloading a specific month, validate the existing data first.

---

# 21. Validate fact_sales

Connect to:

```text
ecommerce_dw
```

Run:

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT orders_item_id) AS distinct_items,
    COUNT(DISTINCT orders_id) AS distinct_orders
FROM dw.fact_sales;
```

The important conditions are:

```text
total_rows = distinct_items
```

and:

```text
distinct_items
```

should represent the number of successfully loaded order items.

---

# 22. Validate by month

Run:

```sql
SELECT
    DATE_TRUNC('month', dd.full_date)::date AS month,
    COUNT(*) AS fact_rows,
    COUNT(DISTINCT fs.orders_item_id) AS distinct_items,
    COUNT(DISTINCT fs.orders_id) AS distinct_orders
FROM dw.fact_sales fs
JOIN dw.dim_date dd
    ON fs.date_key = dd.date_key
GROUP BY 1
ORDER BY 1;
```

Example of a successful result:

```text
month       | fact_rows | distinct_items | distinct_orders
------------+-----------+----------------+----------------
2025-01-01  | 46207     | 46207          | 21101
2025-02-01  | 41737     | 41737          | 19086
2025-03-01  | 46940     | 46940          | 21415
2025-04-01  | 45720     | 45720          | 20855
2025-05-01  | 47661     | 47661          | 21556
```

The exact numbers depend on the amount of generated data.

---

# 23. Validate revenue

Run:

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT orders_item_id) AS distinct_items,
    COUNT(DISTINCT orders_id) AS distinct_orders,
    SUM(quantity) AS total_quantity,
    SUM(subtotal) AS total_subtotal,
    SUM(total_amount) AS total_revenue
FROM dw.fact_sales;
```

The project uses:

```text
subtotal
```

as the primary revenue value for the analytical reports.

Therefore the Power BI `Total Revenue` measure should be:

```DAX
Total Revenue =
SUM('dw fact_sales'[subtotal])
```

Do not use `total_amount` if that column is not populated correctly in the current ETL data.

---

# 24. Validate revenue by status

Run:

```sql
SELECT
    status,
    COUNT(*) AS rows,
    COUNT(DISTINCT orders_id) AS orders,
    SUM(quantity) AS quantity,
    SUM(subtotal) AS revenue
FROM dw.fact_sales
GROUP BY status
ORDER BY status;
```

This allows the analyst to compare:

```text
CANCELLED
DELIVERED
PAID
PLACED
RETURNED
SHIPPED
```

---

# 25. SQL analytics

The project can contain analytical views/functions such as:

```text
vw_fact_sales
vw_products_sales
vw_sales_summary
vw_seller_performance
```

and stored procedures/functions such as:

```text
sp_load_fact_sales
sp_refresh_sales
sp_update_order_total
```

The purpose of these objects is to move common business logic into the database layer and provide optimized datasets for reporting.

---

# 26. Example business queries

### Monthly revenue

```sql
SELECT
    DATE_TRUNC('month', dd.full_date)::date AS month,
    SUM(fs.subtotal) AS revenue
FROM dw.fact_sales fs
JOIN dw.dim_date dd
    ON fs.date_key = dd.date_key
GROUP BY 1
ORDER BY 1;
```

### Revenue by category

```sql
SELECT
    dc.category_name,
    SUM(fs.subtotal) AS revenue
FROM dw.fact_sales fs
JOIN dw.dim_category dc
    ON fs.category_key = dc.category_key
GROUP BY dc.category_name
ORDER BY revenue DESC;
```

### Revenue by seller

```sql
SELECT
    ds.seller_name,
    SUM(fs.subtotal) AS revenue
FROM dw.fact_sales fs
JOIN dw.dim_seller ds
    ON fs.seller_key = ds.seller_key
GROUP BY ds.seller_name
ORDER BY revenue DESC;
```

### Quantity sold by product

```sql
SELECT
    dp.product_name,
    SUM(fs.quantity) AS quantity_sold
FROM dw.fact_sales fs
JOIN dw.dim_product dp
    ON fs.product_key = dp.product_key
GROUP BY dp.product_name
ORDER BY quantity_sold DESC;
```

---

# 27. Power BI connection

Open:

```text
Power BI Desktop
```

Select:

```text
Home
→ Get Data
→ PostgreSQL database
```

Use:

```text
Server:
localhost:5432

Database:
ecommerce_dw
```

Authentication:

```text
Database
```

Username:

```text
nguyendung
```

Password:

```text
<POSTGRES_PASSWORD>
```

Select the Data Warehouse schema:

```text
dw
```

and import/connect to:

```text
dim_brand
dim_category
dim_customer
dim_date
dim_product
dim_seller
fact_sales
```

---

# 28. Power BI data model

The recommended model is:

```text
                 dim_date
                    │
                    │
                    ▼
dim_customer → fact_sales ← dim_product
                    │
                    ├── dim_seller
                    │
                    ├── dim_brand
                    │
                    └── dim_category
```

Relationships should generally be:

```text
Dimension: 1
Fact: *
```

For example:

```text
dim_date[date_key]
        1
        │
        *
fact_sales[date_key]
```

and:

```text
dim_category[category_key]
        1
        │
        *
fact_sales[category_key]
```

---

# 29. Power BI measures

Create the following measures.

### Total Revenue

```DAX
Total Revenue =
SUM('dw fact_sales'[subtotal])
```

### Total Quantity

```DAX
Total Quantity =
SUM('dw fact_sales'[quantity])
```

### Total Orders

```DAX
Total Orders =
DISTINCTCOUNT('dw fact_sales'[orders_id])
```

### Total Order Items

```DAX
Total Order Items =
DISTINCTCOUNT('dw fact_sales'[orders_item_id])
```

### Total Customers

```DAX
Total Customers =
DISTINCTCOUNT('dw fact_sales'[customer_key])
```

---

# 30. Recommended dashboard

The Power BI dashboard can contain the following business views.

## Page 1 — Overview

KPI cards:

```text
Total Revenue
Total Orders
Total Order Items
Total Quantity
Total Customers
```

Charts:

```text
Revenue by Month
Revenue by Category
```

---

## Page 2 — Sales Analysis

Recommended visuals:

```text
Revenue by Month
Orders by Month
Quantity Sold by Month
Revenue by Status
```

Useful slicers:

```text
Date
Status
Category
Brand
Seller
```

---

## Page 3 — Product & Category Analysis

Recommended visuals:

```text
Top Products by Revenue
Top Products by Quantity
Revenue by Category
Quantity by Category
```

This page helps answer:

> Which products and categories generate the most revenue?

---

## Page 4 — Seller Analysis

Recommended visuals:

```text
Revenue by Seller
Orders by Seller
Quantity Sold by Seller
Top Sellers
```

This helps answer:

> Which sellers contribute the most to the business?

---

# 31. Common problems

## Problem 1 — Container name does not exist

Wrong:

```powershell
docker exec -it postgres:17 ...
```

`postgres:17` is an image name, not the container name.

Use:

```powershell
docker ps
```

Then use the actual container name:

```powershell
docker exec -it ecommerce_postgres psql -U nguyendung -d ecommerce_dw
```

---

## Problem 2 — `host.docker.internal` connection error

Airflow runs inside Docker while PostgreSQL is another Docker container.

The connection must be configured correctly.

For this project:

```text
host.docker.internal
port 5432
```

is used for the dblink connection.

Test:

```sql
SELECT *
FROM dblink(
    'host=host.docker.internal
     port=5432
     dbname=ecommerce_oltp
     user=nguyendung
     password=<POSTGRES_PASSWORD>
     options=''-c max_parallel_workers_per_gather=0''',
    $$
        SELECT COUNT(*)
        FROM orders
    $$
) AS t(total_orders BIGINT);
```

---

## Problem 3 — `max_parallel_workers_per_gather` error

If PostgreSQL returns:

```text
-c %20max_parallel_workers_per_gather%3D0 requires a value
```

the connection string was malformed.

Use:

```text
options=''-c max_parallel_workers_per_gather=0''
```

instead of URL-encoded or incorrectly quoted options.

---

## Problem 4 — Fact rows are much lower than source rows

Do not immediately assume the INSERT failed.

Check the dimension tables.

For example:

```sql
SELECT COUNT(*)
FROM dw.dim_customer;
```

Compare with:

```sql
SELECT COUNT(*)
FROM customer;
```

Then check:

```text
customer
product
seller
brand
category
```

A normal SQL `JOIN` removes source rows when a dimension key cannot be found.

Therefore:

```text
Source rows
     ↓
JOIN dim_date
     ↓
JOIN dim_customer
     ↓
JOIN dim_product
     ↓
JOIN dim_seller
     ↓
JOIN dim_brand
     ↓
JOIN dim_category
     ↓
Fact rows
```

All required dimension records must exist before loading the fact table.

---

# 32. Check missing dimension keys

Example for products:

```sql
SELECT COUNT(*) AS missing_products
FROM dblink(
    'host=host.docker.internal
     port=5432
     dbname=ecommerce_oltp
     user=nguyendung
     password=<POSTGRES_PASSWORD>
     options=''-c max_parallel_workers_per_gather=0''',
    $$
        SELECT product_id
        FROM product
    $$
) AS p(product_id INT)
LEFT JOIN dw.dim_product dp
    ON dp.product_id = p.product_id
WHERE dp.product_id IS NULL;
```

Expected:

```text
0
```

The same concept can be applied to:

```text
customer
seller
brand
category
```

---

# 33. Restarting the ETL

If the containers are already running:

```powershell
docker compose up -d
```

Do not unnecessarily recreate the database.

Check:

```powershell
docker ps
```

Then open:

```text
http://localhost:8080
```

and trigger:

```text
ecommerce_dw_etl
```

---

# 34. Resetting fact_sales

Only do this when intentionally rebuilding the Data Warehouse fact table.

Connect to:

```text
ecommerce_dw
```

Then:

```sql
TRUNCATE TABLE dw.fact_sales RESTART IDENTITY;
```

After that, reload the fact data through Airflow.

> Do not run this command if you only want to continue an existing successful ETL run.

---

# 35. Stop the project

Stop containers:

```powershell
docker compose stop
```

Start them again later:

```powershell
docker compose start
```

If you want to stop and remove the containers:

```powershell
docker compose down
```

Be careful with:

```powershell
docker compose down -v
```

because removing volumes can delete PostgreSQL data depending on the Compose configuration.

---

# 36. Useful commands

### List containers

```powershell
docker ps
```

### View PostgreSQL logs

```powershell
docker logs ecommerce_postgres
```

### View Airflow webserver logs

```powershell
docker logs airflow_webserver
```

### View Airflow scheduler logs

```powershell
docker logs airflow_scheduler
```

### Enter PostgreSQL

```powershell
docker exec -it ecommerce_postgres psql -U nguyendung -d ecommerce_dw
```

### Enter OLTP

```powershell
docker exec -it ecommerce_postgres psql -U nguyendung -d ecommerce_oltp
```

### Check Airflow DAG import errors

```powershell
docker exec airflow_webserver airflow dags list-import-errors
```

### List Airflow DAGs

```powershell
docker exec airflow_webserver airflow dags list
```

---

# 37. End-to-end workflow

For someone running the project for the first time, the recommended workflow is:

```text
1. Clone repository
        ↓
2. Start Docker
        ↓
3. Check PostgreSQL
        ↓
4. Check ecommerce_oltp
        ↓
5. Generate transactional data
        ↓
6. Check OLTP row counts
        ↓
7. Prepare ecommerce_dw
        ↓
8. Create/verify dimensions
        ↓
9. Enable dblink
        ↓
10. Test OLTP → DW connection
        ↓
11. Start Airflow
        ↓
12. Open Airflow UI
        ↓
13. Trigger ecommerce_dw_etl
        ↓
14. Load January
        ↓
15. Load February
        ↓
16. Load March
        ↓
17. Load April
        ↓
18. Load May
        ↓
19. Validate fact_sales
        ↓
20. Validate revenue
        ↓
21. Open Power BI
        ↓
22. Connect to ecommerce_dw
        ↓
23. Create relationships
        ↓
24. Create DAX measures
        ↓
25. Build dashboards
```

---

# 38. Data quality checklist

Before considering the project complete, verify:

### OLTP

```text
[ ] orders contains data
[ ] orders_item contains data
[ ] customer contains data
[ ] product contains data
[ ] seller contains data
[ ] brand contains data
[ ] category contains data
```

### Data Warehouse

```text
[ ] dim_date contains required dates
[ ] dim_customer contains source customers
[ ] dim_product contains source products
[ ] dim_seller contains source sellers
[ ] dim_brand contains source brands
[ ] dim_category contains source categories
[ ] fact_sales contains data
```

### ETL

```text
[ ] ecommerce_dw_etl imports successfully
[ ] check_oltp succeeds
[ ] each monthly load succeeds
[ ] validate_dw succeeds
[ ] no unexpected duplicate orders_item_id
[ ] monthly fact counts are reasonable
```

### Power BI

```text
[ ] PostgreSQL connection succeeds
[ ] relationships are correct
[ ] Total Revenue is not zero
[ ] Total Orders is correct
[ ] Total Quantity is correct
[ ] monthly revenue chart works
[ ] category chart works
[ ] filters/slicers work
```

---

# 39. Final result

After completing the project, the final architecture is:

```text
                   ┌──────────────────────┐
                   │  Python Data         │
                   │  Generator           │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   ecommerce_oltp     │
                   │                      │
                   │ Orders               │
                   │ Order Items          │
                   │ Customers            │
                   │ Products             │
                   │ Sellers              │
                   │ Brands               │
                   │ Categories           │
                   └──────────┬───────────┘
                              │
                              │ dblink
                              │
                              ▼
                   ┌──────────────────────┐
                   │      Airflow         │
                   │                      │
                   │ ecommerce_dw_etl     │
                   │                      │
                   │ Monthly ETL          │
                   │ Validation           │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │    ecommerce_dw      │
                   │                      │
                   │    Star Schema       │
                   │                      │
                   │ fact_sales           │
                   │ dim_date             │
                   │ dim_customer         │
                   │ dim_product          │
                   │ dim_seller           │
                   │ dim_brand            │
                   │ dim_category         │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │      Power BI        │
                   │                      │
                   │ KPI Dashboard        │
                   │ Revenue Analysis     │
                   │ Product Analysis     │
                   │ Seller Analysis      │
                   └──────────────────────┘
```

The project demonstrates a complete Data Engineering pipeline:

```text
Data Generation
      +
OLTP Database
      +
ETL Orchestration
      +
Data Warehouse
      +
Data Validation
      +
Business Analytics
      +
Power BI
```

This makes the project suitable as a portfolio project for demonstrating practical skills in **Python, SQL, PostgreSQL, Docker, Apache Airflow, Data Warehousing, ETL, dimensional modeling and Power BI**.
