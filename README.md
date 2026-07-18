# Ecommerce OLTP Data Generator

A Python-based synthetic data generator for an e-commerce OLTP database system.

This project simulates a real-world e-commerce transactional database by generating realistic test data for customers, sellers, products, promotions, orders, and order items.

The generated dataset is designed for Data Engineering practice, including:
- ETL pipeline development
- Data warehouse modeling
- SQL analytics
- Database optimization
- Data processing experiments
---

# Project Overview

The goal of this project is to build a complete OLTP data generation system similar to an e-commerce platform.

The system automatically creates:

- Customers
- Sellers
- Brands
- Categories
- Products
- Promotions
- Promotion-product relationships
- Orders
- Order items


The generated data maintains:

- Primary key relationships
- Foreign key constraints
- Data validation rules
- Realistic distributions
- Business logic consistency


---

# Architecture







## Run with Docker

docker compose up --build


## Running with Docker
git clone https://github.com/Dungguyen/Ecommerce-oltp-data-generator-unigap.git

cd Ecommerce-oltp-data-generator-unigap

## Environment Setup

Create .env file:
+ cp .env.example .env

## Start Application
+ docker compose up --build

## Running Without Docker

+ uv sync
+ uv run python main.py
## Main tables:


| Table | Description |
|---|---|
| customer | Customer information |
| seller | Marketplace sellers |
| brand | Product brands |
| category | Product categories |
| product | Product catalog |
| promotion | Discount campaigns |
| promotion_product | Product promotion mapping |
| orders | Customer transactions |
| orders_item | Order details |


# Project Structure
│
├── config/
│ └── Database configuration

├── data/
│ ├── Constants
│ ├── Product catalog
│ └── Business rules

├── generators/
│ ├── brand_generator.py
│ ├── category_generator.py
│ ├── seller_generator.py
│ ├── customer_generator.py
│ ├── product_generator.py
│ ├── promotion_generator.py
│ ├── orders_generator.py
│ └── orders_item_generator.py

├── sql/
│ └── create_tables.sql

├── utils/
│ ├── faker_utils.py
│ └── logger.py

├── main.py

├── Dockerfile

├── docker-compose.yml

├── pyproject.toml

├── uv.lock

├── .env.example

└── README.md

# Features


## Synthetic Data Generation

The project generates realistic data using:

- Faker library
- Business rules
- Weighted random sampling


