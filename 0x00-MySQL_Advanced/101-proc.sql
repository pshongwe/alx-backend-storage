USE holberton;

-- Create the procedure to compute average weighted score for a single user
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;

    -- Calculate the total weighted score and total weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_weighted_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Compute the average weighted score
    IF total_weight > 0 THEN
        SET total_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET total_weighted_score = 0;
    END IF;

    -- Update the average_score in the users table
    UPDATE users
    SET average_score = total_weighted_score
    WHERE id = user_id;
END;

//

DELIMITER ;

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

