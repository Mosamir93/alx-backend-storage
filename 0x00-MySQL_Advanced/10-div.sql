-- Script to create a function SafeDiv that divides two numbers and returns the result or 0 if the divisor is 0
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END; //
DELIMITER ;
