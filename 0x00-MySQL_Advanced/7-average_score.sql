-- script creates a stored procedure
-- that computes and store the average score of a student
-- an average score can be a decimal
-- procedure is taking 1 input and is linking to an existing users
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE num_corrections INT;
    DECLARE avg_score FLOAT;
    

    SELECT SUM(score), COUNT(*)
    INTO total_score, num_corrections
    FROM corrections
    WHERE user_id = user_id;

    IF num_corrections > 0 THEN
	SET avg_score = total_score / num_corrections;
	UPDATE users
	SET average_score = avg_score
	WHERE id = user_id;
    END IF;
END $$
DELIMITER ;
