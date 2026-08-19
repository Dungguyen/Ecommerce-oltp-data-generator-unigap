# Optimization Report

## 1. Overview

This document records the query optimization process for the Ecommerce OLTP database.

The optimization process consists of:

1. Running the original query and capturing its execution plan and execution time.
2. Applying partitioning and indexing techniques.
3. Re-running the same query.
4. Capturing the optimized execution plan and execution time.
5. Comparing the performance before and after optimization.

### Optimization techniques

* Monthly partitioning for `orders`
* Monthly partitioning for `orders_item`
* Index on `orders_item(product_id)`
* Execution plan analysis using PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`

---

# 2. Query Optimization

## Query 1 – Total Revenue per Month

### Requirement

Calculate total revenue for each month.

### Query

```sql
SELECT
    DATE_TRUNC('month', orders_date)::date AS month,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY 1
ORDER BY 1;
```

### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    DATE_TRUNC('month', orders_date)::date AS month,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY 1
ORDER BY 1;
```

### Execution Plan – Before

> Paste the output of `EXPLAIN (ANALYZE, BUFFERS)` here.

```text
PASTE BEFORE EXECUTION PLAN HERE
```

**Execution Time:** `___206.099__ ms`

### Optimization

Monthly partitioning was applied to the `orders` table for January–May 2025.

### After Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    DATE_TRUNC('month', orders_date)::date AS month,
    SUM(total_amount) AS total_revenue
FROM orders
GROUP BY 1
ORDER BY 1;
```

### Execution Plan – After

```text
PASTE AFTER EXECUTION PLAN HERE
```

**Execution Time:** `__141.728___ ms`

### Comparison

| Metric         | Before |  After |
| -------------- | -----:     | -----:     |
| Execution Time | 206.099 ms | 141.728 ms |
| Planning Time  | 0.081 ms | 1.566 ms |
| Scan Method    |  ___   |    ___ |
| Buffers Read   |  ____  |    ___ |

---

# Query 2 – Orders Filtered by Seller and Date

### Requirement

Retrieve orders belonging to a specific seller within a specific date range.

### Query

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    o.orders_id,
    o.orders_date,
    o.customer_id,
    oi.product_id,
    oi.quantity,
    oi.subtotal
FROM orders o
JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date
JOIN product p
    ON p.product_id = oi.product_id
WHERE p.seller_id = 5495
  AND o.orders_date >= '2025-03-01'
  AND o.orders_date < '2025-04-01';
```

### Before Optimization

```sql


```

### Execution Plan – Before

```text
Gather  (cost=1013.47..10285.05 rows=1 width=32) (actual time=1.285..81.798 rows=236 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   Buffers: shared hit=13668 read=4832
   ->  Nested Loop  (cost=13.47..9284.95 rows=1 width=32) (actual time=1.567..40.232 rows=79 loops=3)
         Buffers: shared hit=13668 read=4832
         ->  Hash Join  (cost=13.05..8576.17 rows=1428 width=28) (actual time=0.904..35.169 rows=1063 loops=3)
               Hash Cond: (oi.product_id = p.product_id)
               Buffers: shared hit=914 read=4832
               ->  Parallel Seq Scan on orders_item oi  (cost=0.00..7957.08 rows=229008 width=28) (actual time=0.388..20.526 rows=183206 loops=3)
                     Buffers: shared hit=835 read=4832
               ->  Hash  (cost=13.01..13.01 rows=3 width=4) (actual time=0.371..0.371 rows=3 loops=3)
                     Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                                                
                     Buffers: shared hit=21                                                                                                                                      
                     ->  Seq Scan on product p  (cost=0.00..13.01 rows=3 width=4) (actual time=0.317..0.365 rows=3 loops=3)                                                      
                           Filter: (seller_id = 5495)                                                                                                                            
                           Rows Removed by Filter: 518                                                                                                                           
                           Buffers: shared hit=21                                                                                                                                
         ->  Index Scan using orders_pkey on orders o  (cost=0.42..0.49 rows=1 width=16) (actual time=0.004..0.004 rows=0 loops=3188)                                            
               Index Cond: (orders_id = oi.orders_id)                                                                                                                            
               Filter: ((orders_date >= '2025-03-01 00:00:00'::timestamp without time zone) AND (orders_date < '2025-04-01 00:00:00'::timestamp without time zone) AND (oi.orders_date = orders_date))                                                                                                                                                             
               Rows Removed by Filter: 1                                                                                                                                         
               Buffers: shared hit=12754   
```

**Execution Time:** `__81.866___ ms`

### Optimization

Monthly partitions allow PostgreSQL to eliminate partitions outside the requested date range.

### After Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)

```

### Execution Plan – After

```text
 Gather  (cost=1013.47..10285.05 rows=1 width=32) (actual time=1.226..77.685 rows=236 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   Buffers: shared hit=13764 read=4736
   ->  Nested Loop  (cost=13.47..9284.95 rows=1 width=32) (actual time=1.967..38.308 rows=79 loops=3)
         Buffers: shared hit=13764 read=4736
         ->  Hash Join  (cost=13.05..8576.17 rows=1428 width=28) (actual time=0.734..33.518 rows=1063 loops=3)
               Hash Cond: (oi.product_id = p.product_id)
               Buffers: shared hit=1010 read=4736
               ->  Parallel Seq Scan on orders_item oi  (cost=0.00..7957.08 rows=229008 width=28) (actual time=0.300..19.459 rows=183206 loops=3)
                     Buffers: shared hit=931 read=4736
               ->  Hash  (cost=13.01..13.01 rows=3 width=4) (actual time=0.341..0.342 rows=3 loops=3)
                     Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                                                
                     Buffers: shared hit=21                                                                                                                                      
                     ->  Seq Scan on product p  (cost=0.00..13.01 rows=3 width=4) (actual time=0.288..0.337 rows=3 loops=3)                                                      
                           Filter: (seller_id = 5495)                                                                                                                            
                           Rows Removed by Filter: 518                                                                                                                           
                           Buffers: shared hit=21                                                                                                                                
         ->  Index Scan using orders_pkey on orders o  (cost=0.42..0.49 rows=1 width=16) (actual time=0.004..0.004 rows=0 loops=3188)                                            
               Index Cond: (orders_id = oi.orders_id)                                                                                                                            
               Filter: ((orders_date >= '2025-03-01 00:00:00'::timestamp without time zone) AND (orders_date < '2025-04-01 00:00:00'::timestamp without time zone) AND (oi.orders_date = orders_date))                                                                                                                                                             
               Rows Removed by Filter: 1                                                                                                                                         
               Buffers: shared hit=12754      
```

**Execution Time:** `__77.753___ ms`

---

# Query 3 – Filter order_item by product_id

### Requirement

Find order items belonging to a specific product.

### Query

### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    orders_item_id,
    orders_id,
    orders_date,
    quantity,
    unit_price,
    subtotal
FROM orders_item
WHERE product_id = 121;
```

### Execution Plan – Before

 Bitmap Heap Scan on orders_item  (cost=12.55..2680.28 rows=1048 width=40) (actual time=0.269..1.005 rows=1122 loops=1)
   Recheck Cond: (product_id = 121)
   Heap Blocks: exact=1007
   Buffers: shared hit=1011
   ->  Bitmap Index Scan on idx_orders_item_product_id  (cost=0.00..12.29 rows=1048 width=0) (actual time=0.144..0.145 rows=1122 loops=1)
         Index Cond: (product_id = 121)
         Buffers: shared hit=4
 Planning Time: 0.089 ms
```

**Execution Time:** `1.071 ms`

### Optimization

An index was created on `orders_item(product_id)`:

```sql
CREATE INDEX idx_orders_item_product_id
ON orders_item(product_id);
```

### After Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    orders_item_id,
    orders_id,
    orders_date,
    quantity,
    unit_price,
    subtotal
FROM orders_item
WHERE product_id = 121;
```

### Execution Plan – After

```text
Bitmap Heap Scan on orders_item  (cost=12.55..2680.28 rows=1048 width=40) (actual time=0.264..3.070 rows=1122 loops=1)
   Recheck Cond: (product_id = 121)
   Heap Blocks: exact=1007
   Buffers: shared hit=1011
   ->  Bitmap Index Scan on idx_orders_item_product_id  (cost=0.00..12.29 rows=1048 width=0) (actual time=0.148..0.148 rows=1122 loops=1)
         Index Cond: (product_id = 121)
         Buffers: shared hit=4
 Planning:
   Buffers: shared hit=100
 Planning Time: 2.409 ms

**Execution Time:** `3.218 ms`

### Expected Optimization Behavior

Before optimization, PostgreSQL may perform a sequential scan:

```text
Seq Scan on orders_item
```

After creating the index, PostgreSQL may choose an index-based access path:

```text
Index Scan using idx_orders_item_product_id
```

The actual plan should be taken from the PostgreSQL execution output.

---

# Query 4 – Find Order with Highest total_amount

### Requirement

Find the order with the highest total amount.

### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    orders_id,
    orders_date,
    customer_id,
    total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 1;
```

### Execution Plan – Before

```text

```

**Execution Time:** `63.807 ms`

### Optimization

No additional index is required specifically for this query unless the execution plan demonstrates that sorting is a significant bottleneck.

### After Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    orders_id,
    orders_date,
    customer_id,
    total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 1;
```

### Execution Plan – After

**Execution Time:** `63.051 ms`

---

# Query 5 – Products with Highest Quantity Sold

### Requirement

Find products with the highest quantity sold.


### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    oi.product_id,
    SUM(oi.quantity) AS total_quantity
FROM orders_item oi
JOIN orders o
    ON o.orders_id = oi.orders_id
   AND o.orders_date = oi.orders_date
GROUP BY oi.product_id
ORDER BY total_quantity DESC
LIMIT 5;
```

### Execution Plan – Before


**Execution Time:** `310.751 ms`

### After Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    oi.product_id,
    SUM(oi.quantity) AS total_quantity
FROM orders_item oi
JOIN orders o
    ON o.orders_id = oi.orders_id
   AND o.orders_date = oi.orders_date
GROUP BY oi.product_id
ORDER BY total_quantity DESC
LIMIT 10;
```

### Execution Plan – After


**Execution Time:** `312.997 ms`

---

# Query 6 – Orders by Seller in March 2025

### Requirement

Calculate the number of orders handled by each seller in March 2025.

### Query

```sql
SELECT
    p.seller_id,
    COUNT(DISTINCT o.orders_id) AS total_orders
FROM orders o
JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date
JOIN product p
    ON p.product_id = oi.product_id
WHERE o.orders_date >= '2025-03-01'
  AND o.orders_date < '2025-04-01'
GROUP BY p.seller_id
ORDER BY total_orders DESC;
```

### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    p.seller_id,
    COUNT(DISTINCT o.orders_id) AS total_orders
FROM orders o
JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date
JOIN product p
    ON p.product_id = oi.product_id
WHERE o.orders_date >= '2025-03-01'
  AND o.orders_date < '2025-04-01'
GROUP BY p.seller_id
ORDER BY total_orders DESC;
```

### Execution Plan – Before

 Sort  (cost=16163.88..16163.89 rows=1 width=12) (actual time=128.964..129.341 rows=501 loops=1)
   Sort Key: (count(DISTINCT o.orders_id)) DESC
   Sort Method: quicksort  Memory: 44kB
   Buffers: shared hit=147611 read=3325
   ->  GroupAggregate  (cost=16163.85..16163.87 rows=1 width=12) (actual time=123.027..129.225 rows=501 loops=1)
         Group Key: p.seller_id
         Buffers: shared hit=147611 read=3325
         ->  Sort  (cost=16163.85..16163.86 rows=1 width=8) (actual time=123.007..125.312 rows=46940 loops=1)
               Sort Key: p.seller_id, o.orders_id
               Sort Method: quicksort  Memory: 3003kB
               Buffers: shared hit=147611 read=3325
               ->  Nested Loop  (cost=7004.35..16163.84 rows=1 width=8) (actual time=25.331..102.361 rows=46940 loops=1)
                     Buffers: shared hit=147611 read=3325                                                                                                              
                     ->  Gather  (cost=7004.08..16163.55 rows=1 width=8) (actual time=25.304..47.808 rows=46940 loops=1)                                                         
                           Workers Planned:2                                                                                                                                    
                           Workers Launched: 2                                                                                                                                   
                           Buffers: shared hit=6791 read=3325                                                                                                                    
                           ->  Parallel Hash Join  (cost=6004.08..15163.45 rows=1 width=8) (actual time=8.639..45.886 rows=15647 loops=3)                                        
                                 Hash Cond: ((oi.orders_id = o.orders_id) AND (oi.orders_date = o.orders_date))                                                                  
                                 Buffers: shared hit=6791 read=3325                                                                                                              
                                 ->  Parallel Seq Scan on orders_item oi  (cost=0.00..7957.08 rows=229008 width=16) (actual time=0.149..15.625 rows=183206 loops=3)              
                                       Buffers: shared hit=2342 read=3325                                                                                                        
                                 ->  Parallel Hash  (cost=5869.50..5869.50 rows=8972 width=12) (actual time=8.295..8.295 rows=7138 loops=3)                                      
                                       Buckets: 32768  Batches: 1  Memory Usage: 1280kB                                                                                          
                                       Buffers: shared hit=4307                                                                                                                  
                                       ->  Parallel Seq Scan on orders o  (cost=0.00..5869.50 rows=8972 width=12) (actual time=0.433..20.429 rows=21415 loops=1)                 
                                             Filter: ((orders_date >= '2025-03-01 00:00:00'::timestamp without time zone) AND (orders_date < '2025-04-01 00:00:00'::timestamp without time zone))                                                                                                                                                                  
                                             Rows Removed by Filter: 228585                                                                                                      
                                             Buffers: shared hit=4307                                                                                                            
                     ->  Index Scan using product_pkey on product p  (cost=0.27..0.29 rows=1 width=8) (actual time=0.001..0.001 rows=1 loops=46940)                              
                           Index Cond: (product_id = oi.product_id)                                                                                                              
                           Buffers: shared hit=140820                                                                                                                            
 Planning:                                                                                                                                                                       
   Buffers: shared hit=18                                                                                                                                                        
 Planning Time: 0.318 ms   

**Execution Time:** `129.547 ms`

### After Optimization

**Execution Time:** `122.021 ms`

---

# Query 7 – Revenue per Product per Month

### Requirement

Calculate monthly revenue for each product.

### Query

```sql
SELECT
    DATE_TRUNC('month', o.orders_date)::date AS month,
    oi.product_id,
    SUM(oi.subtotal) AS total_revenue
FROM orders o
JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date
GROUP BY
    DATE_TRUNC('month', o.orders_date)::date,
    oi.product_id
ORDER BY month, total_revenue DESC;
```

### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    DATE_TRUNC('month', o.orders_date)::date AS month,
    oi.product_id,
    SUM(oi.subtotal) AS total_revenue
FROM orders o
JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date
GROUP BY
    DATE_TRUNC('month', o.orders_date)::date,
    oi.product_id
ORDER BY month, oi.product_id DESC;
```

### Execution Plan – Before

**Execution Time:** `504.375 ms`

### After Optimization

**Execution Time:** `468.889 ms`

---

# Query 8 – Products Sold per Seller

### Requirement

Calculate the total quantity sold by each seller.

### Query

```sql
SELECT
    p.seller_id,
    SUM(oi.quantity) AS total_quantity
FROM orders_item oi
JOIN product p
    ON p.product_id = oi.product_id
GROUP BY p.seller_id
ORDER BY total_quantity DESC;
```

### Before Optimization

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    p.seller_id,
    SUM(oi.quantity) AS total_quantity
FROM orders_item oi
JOIN product p
    ON p.product_id = oi.product_id
GROUP BY p.seller_id
ORDER BY total_quantity DESC;
```

### Execution Plan – Before

**Execution Time:** `110.353 ms`

### After Optimization

**Execution Time:** `108.417 ms`

---

# 3. Overall Performance Comparison

After all queries have been executed before and after optimization, summarize the results below.

| Query                           | Before (ms) | After (ms) | Improvement |
| ------------------------------- | ----------: | ---------: | ----------: |
| Total Revenue per Month         |    206.099  |    141.728 |      32.23% |
| Orders by Seller + Date         |      81.866 |     77.753 |       5,02% |
| Filter order_item by product_id |       1.071 |      3.218 |       -300% |
| Highest total_amount            |      63.807 |    63.051  |       1,25% |
| Highest Quantity Sold           |     310.751 |    312.997 |      -3,44% |
| Orders by Seller in March       |      129.547|    122.021 |       5.79% |
| Revenue per Product per Month   |     504.375 |     468.889|       6,64% |
| Products Sold per Seller        |     110.353 |    108.417 |       1,72% |


# 4. Optimization Summary

The project applies two main PostgreSQL optimization techniques.

## 4.1 Monthly Partitioning

The `orders` and `orders_item` tables are partitioned by month for the period:

* January 2025
* February 2025
* March 2025
* April 2025
* May 2025

Partitioning allows PostgreSQL to reduce the amount of data scanned when a query contains a date filter.

For example:

```sql
WHERE orders_date >= '2025-03-01'
  AND orders_date < '2025-04-01'
```

can allow PostgreSQL to access only the relevant March partition instead of scanning the entire table.

## 4.2 Index on order_item(product_id)

An index was created on:

```sql
CREATE INDEX idx_orders_item_product_id
ON orders_item(product_id);
```

This optimization targets queries that filter or join using `product_id`.

---

# 5. Execution Plan Analysis

The main indicators used when comparing execution plans are:

### Execution Time

Lower execution time indicates better query performance.

### Scan Method

Compare:

```text
Seq Scan
```

against:

```text
Index Scan
Index Only Scan
Bitmap Index Scan
```

### Partition Pruning

For date-filtered queries, verify whether PostgreSQL accesses only the relevant partitions.

### Buffers

Compare:

```text
Buffers: shared hit
Buffers: shared read
```

Lower disk reads generally indicate less I/O work.

### Planning Time

Planning time may increase slightly because PostgreSQL evaluates partitions and indexes. The important metric is the overall execution performance.

---

# 6. Conclusion

The optimization process demonstrates how PostgreSQL partitioning and indexing can improve query performance on a large Ecommerce OLTP database.

Monthly partitioning is particularly useful for time-range queries, while the `product_id` index improves product-based filtering and lookup operations.

The execution plans recorded in this document provide evidence of how PostgreSQL changes its query execution strategy before and after optimization.
