-- Task 4: Buy buy buy
-- This script creates a trigger to decrease the quantity of an item after adding a new order.
CREATE TRIGGER update_quantity AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
