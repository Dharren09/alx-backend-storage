-- script creates a trigger that decreases the quantity of an item
-- by adding a new order
-- quantity in the table can be negative
DROP TRIGGER IF EXISTS decrease_quantity;
DELIMITER $$
CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE id = NEW.item_id;
END $$
DELIMITER ;
