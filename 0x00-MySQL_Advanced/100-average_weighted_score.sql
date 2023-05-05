-- script that creates a stored procedure
-- that computes and store the avg weighted score for a student
-- procedure takes 1 input
-- assuming the value is linked to the existing users
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score INT;
    DECLARE total_weight INT;
    DECLARE average_score FLOAT;
    
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
END $$
DELIMITER ;
