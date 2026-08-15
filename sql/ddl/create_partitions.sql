-- =========================================================
-- PARTITION SETUP
-- PostgreSQL
-- Date range: 2025-01-01 -> 2025-06-01
-- =========================================================    
BEGIN;

-- =========================================================
-- 1. Rename existing tables
-- =========================================================

ALTER TABLE orders
RENAME TO orders_old;

ALTER TABLE orders_item
RENAME TO orders_item_old;

-- =========================================================
-- 2. Create partitioned orders table
-- =========================================================

CREATE TABLE orders
(
    orders_id INT NOT NULL,
    customer_id INT NOT NULL,
    orders_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status varchar(20) not null,
    total_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,

    CONSTRAINT orders_pkey
        PRIMARY KEY (orders_id, orders_date),

    CONSTRAINT chk_status
        CHECK (
            status IN (
                'PLACED',
                'PAID',
                'SHIPPED',
                'DELIVERED',
                'CANCELLED',
                'RETURNED'
            )
        ),
    
    CONSTRAINT chk_total_amount
        CHECK (total_amount >= 0 ),

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
)

PARTITION BY RANGE (orders_date);


-- =========================================================
-- 3. Create monthly partitions for orders
-- =========================================================

CREATE TABLE orders_2025_01
PARTITION OF orders
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');


CREATE TABLE orders_2025_02
PARTITION OF orders
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');


CREATE TABLE orders_2025_03
PARTITION OF orders
FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');


CREATE TABLE orders_2025_04
PARTITION OF orders
FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');


CREATE TABLE orders_2025_05
PARTITION OF orders
FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');


COMMIT;


-- =========================================================
-- STEP 03
-- Create partitioned orders_item table
-- =========================================================

BEGIN;

CREATE TABLE orders_item
(
    orders_item_id BIGINT NOT NULL,
    orders_id INT NOT NULL,
    product_id INT NOT NULL,
    orders_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0),

    subtotal DECIMAL(12,2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED,

    created_at TIMESTAMP NOT NULL,

    CONSTRAINT orders_item_pkey
        PRIMARY KEY (orders_item_id, orders_date),

    CONSTRAINT fk_order
        FOREIGN KEY (orders_id, orders_date)
        REFERENCES orders (orders_id, orders_date)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_created_at
        CHECK (created_at >= orders_date)
)
PARTITION BY RANGE (orders_date);


CREATE TABLE orders_item_2025_01
PARTITION OF orders_item
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE orders_item_2025_02
PARTITION OF orders_item
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

CREATE TABLE orders_item_2025_03
PARTITION OF orders_item
FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');

CREATE TABLE orders_item_2025_04
PARTITION OF orders_item
FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');

CREATE TABLE orders_item_2025_05
PARTITION OF orders_item
FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');

COMMIT;
