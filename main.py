from utils.db_utils import get_db_connection
from generators.brand_generator import insert_brands
from generators.category_generator import insert_categories
from generators.seller_generator import insert_sellers
from generators.customer_generator import insert_customers
from generators.product_generator import insert_products
from generators.promotion_generator import insert_promotions
from generators.promotion_product_generator import insert_promotion_products
from generators.orders_generator import insert_orders
from generators.orders_item_generator import insert_orders_items


def main():
    conn = get_db_connection()
    try:
        insert_brands(conn)
        insert_categories(conn)
        insert_sellers(conn)
        insert_customers(conn)
        insert_products(conn)
        insert_promotions(conn)
        insert_promotion_products(conn)
        insert_orders(conn)
        insert_orders_items(conn)

    finally:    
        conn.close()


if __name__ == "__main__":
    main()
