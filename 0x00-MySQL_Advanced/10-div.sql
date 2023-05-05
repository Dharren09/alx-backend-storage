-- script creates function that divides (and returns) the first
-- by the second number or returns 0 if tthe second
-- number is equal to 0
-- function takes two args
DROP FUNCTION if exists SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;
    
    IF b = 0 THEN
	SET result = 0;
    ELSE
	SET result = a / b;
    END IF;

    RETURN result;
END $$
DELIMITER ;
