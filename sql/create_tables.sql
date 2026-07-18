CREATE TABLE IF NOT EXISTS brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL UNIQUE,
    coutry VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOT NULL
);
--------------------------
CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    parent_category_id INT,
    level SMALLINT NOT NULL CHECK (level IN(1,2)),
    created_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_parent_category
        FOREIGN KEY (parent_category_id)
        REFERENCES category(category_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
---------------------------
CREATE TABLE IF NOT EXISTS seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(150) NOT NULL,
    join_date DATE NOT NULL,
    seller_type VARCHAR(50) NOT NULL),
    rating DECIMAL(2, 1) NOT NULL,
    country VARCHAR(50) NOT NULL,

    CONSTRAINT chk_seller_type CHECK (seller_type IN ('Official', 'Marketing')),
    CONSTRAINT chk_rating CHECK (rating >= 0 AND rating <= 5)
);
---------------------------
CREATE TABLE IF NOT EXISTS customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    gender varchar(10),
    address varchar(255),
    city VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT ,

    CONSTRAINT chk_gender CHECK (gender IN ('Male', 'Female')   )
);
---------------------------
CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    brand_id INT NOT NULL, 
    seller_id INT NOT NULL,
    price DECIMAL(12, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0),
    rating DECIMAL(2, 1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP NOT NULL DEFAULT ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_brand
        FOREIGN KEY (brand_id)
        REFERENCES brand(brand_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES category(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_seller
        FOREIGN KEY (seller_id)
        REFERENCES seller(seller_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
---------------------------
CREATE TABLE IF NOT EXISTS orders(
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT ,
    status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT ,

    CONSTRAINT chk_status CHECK (status IN ('PLACED','PAID','SHIPPED', 'DELIVERED', 'CANCELLED','RETURNED')),
    CONSTRAINT chk_total_amount CHECK (total_amount >= 0),
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
---------------------------
CREATE TABLE IF NOT EXISTS order_item (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT ,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL CHECK (unit_price >= 0),
    subtotal DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at TIMESTAMP NOT NULL DEFAULT,

    CONSTRAINT fk_order
        FOREIGN KEY (order_id)
        REFERENCES "order"(order_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
    CONSTRAINT chk_created_at CHECK (created_at >= order_date)  
);
---------------------------
CREATE TABLE IF NOT EXISTS promotion (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100) NOT NULL,
    promotion_type VARCHAR(50) NOT NULL,
    discount_type VARCHAR(20) NOT NULL CHECK (discount_type IN ('percentage', 'fixed_amount')),
    discount_value NUMERIC(12, 2) NOT NULL CHECK (discount_value >= 0 AND (discount_type = 'fixed_amount' OR discount_value <= 100)),
    start_date DATE NOT NULL CHECK(start_date >= DATE(created_at)),
    end_date DATE NOT NULL CHECK (end_date >= start_date),
    created_at TIMESTAMP NOT NULL DEFAULT
);
---------------------------
CREATE TABLE IF NOT EXISTS promotion_product (
    promo_product_id SERIAL NOT NULL,
    promotion_id INT NOT NULL,
    product_id INT NOT NULL,
    created_At TIMESTAMP NOT NULL DEFAULT,
    PRIMARY KEY (promo_product_id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_promotion_id
        FOREIGN KEY (promotion_id)
        REFERENCES promotion(promotion_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
    CONSTRAINT uq_promotion_product UNIQUE (promotion_id, product_id)

);
----------------------------
