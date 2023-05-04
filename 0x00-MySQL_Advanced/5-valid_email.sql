-- script creates a trigger that resets the attr. valid email
-- only when the email has been changed
DELIMITER $$
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF old.email != new.email THEN
        SET new.valid_email = 0;
    END IF;
END $$
DELIMITER ;
