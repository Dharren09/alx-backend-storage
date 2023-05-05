-- script that creates a stored procedure
-- that computes and stores the average weighted score for all students
-- proceedure is not taking any input
-- calculates using Calculate-Weighted-Average
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_score INT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;
    DECLARE user_id INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;

    -- Loop through all users and compute their average weighted score
    users_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE users_loop;
        END IF;

        -- Compute the total weighted score for the given user
        SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
        INTO total_score, total_weight
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Compute the average weighted score and update the users table
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;

        UPDATE users
        SET average_score = average_score
        WHERE id = user_id;
    END LOOP;

    CLOSE cur;
END $$
DELIMITER ;
