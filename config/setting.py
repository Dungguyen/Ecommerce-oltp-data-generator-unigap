"""
Global settings for the Ecommerce OLTP Data Generator.
"""

from datetime import datetime

# ==========================================================
# Faker
# ==========================================================

FAKER_LOCALE = "vi_VN"

# ==========================================================
# Fixed values
# ==========================================================

DEFAULT_COUNTRY = "Vietnam"

# ==========================================================
# Initial dimension tables
# ==========================================================

NUM_BRANDS = 30
NUM_CATEGORIES = 27
NUM_SELLERS = 500
NUM_CUSTOMERS = 5000

# ==========================================================
# Fact tables
# ==========================================================

NUM_PRODUCTS = 20_000

NUM_ORDERS = 5_000_000

NUM_PROMOTIONS = 100

# ==========================================================
# Batch configuration
# ==========================================================

BATCH_SIZE = 10_000

COMMIT_EVERY_BATCH = True

# ==========================================================
# Promotion configurations
# ==========================================================
MIN_PRODUCTS_PER_PROMOTION = 20
MAX_PRODUCTS_PER_PROMOTION = 100
# ==========================================================
# Order Item configuration
# ==========================================================

MIN_ITEMS_PER_ORDER = 2
MAX_ITEMS_PER_ORDER = 5

# ==========================================================
# Product configuration
# ==========================================================

PRODUCTS_PER_BRAND = 40

# ==========================================================
# Date range
# ==========================================================
PROMOTION_CREATED_START = datetime(2024, 1, 1)
PROMOTION_CREATED_END = datetime(2024, 6, 30)
# ==========================================================
# Promotion configuration
# ==========================================================

MIN_ITEMS_PER_ORDER = 2
MAX_ITEMS_PER_ORDER = 5

# ==========================================================
# order item configuration
# ==========================================================
ORDER_START_DATE = datetime(2025, 1, 1)

ORDER_END_DATE = datetime(2025, 5, 31, 23, 59, 59)

DATA_START_DATE = datetime(2024, 1, 1)

DATA_END_DATE = datetime(2024, 12, 31)

STREAM_FETCH_SIZE = 50000