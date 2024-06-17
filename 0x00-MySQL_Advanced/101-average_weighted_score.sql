-- Create the stored procedure to compute average 
-- weighted score for all users
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD temp_total_weighted_score INT NOT NULL;
    ALTER TABLE users ADD temp_total_weight INT NOT NULL;

    UPDATE users
        SET temp_total_weighted_score = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
        );

    UPDATE users
        SET temp_total_weight = (
            SELECT SUM(projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
        );

    UPDATE users
        SET users.average_score = IF(users.temp_total_weight = 0, 0, users.temp_total_weighted_score / users.temp_total_weight);

    ALTER TABLE users
        DROP COLUMN temp_total_weighted_score;
    ALTER TABLE users
        DROP COLUMN temp_total_weight;
END $$

DELIMITER ;
