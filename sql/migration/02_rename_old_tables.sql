BEGIN;

ALTER TABLE orders
RENAME TO orders_old;

ALTER TABLE orders_item
RENAME TO orders_item_old;

COMMIT;