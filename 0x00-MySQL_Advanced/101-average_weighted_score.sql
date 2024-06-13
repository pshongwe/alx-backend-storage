-- Create the stored procedure to compute average 
-- weighted score for all users
CREATE PROCEDURE ComputeAverageWeightedScoreForUser()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
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

        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_weighted_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = userId;

        IF total_weight > 0 THEN
            SET total_weighted_score = total_weighted_score / total_weight;
        ELSE
            SET total_weighted_score = 0;
        END IF;

        UPDATE users
        SET average_score = total_weighted_score
        WHERE id = userId;
    END LOOP;

    CLOSE userCursor;
END $$
DELIMITER ;
