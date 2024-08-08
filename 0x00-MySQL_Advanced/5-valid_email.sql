-- Task 5: Email validation to sent
-- This script creates a trigger to reset the valid_email attribute when the email has been changed.
DELIMITER $
CREATE TRIGGER email_validation BEFORE UPDATE ON users
FOR EACH ROW
IF NEW.email != OLD.email THEN
    set NEW.valid_email = 0;
END IF$
