-- Create the stored procedure to compute average weighted score for all users
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE userId INT;
    DECLARE userCursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN userCursor;
    read_loop: LOOP
        FETCH userCursor INTO userId;
        IF done THEN
            LEAVE read_loop;
        END IF;

        CALL ComputeAverageWeightedScoreForUser(userId);
    END LOOP;

    CLOSE userCursor;
END;

//

DELIMITER ;
