-- script creates a stored procedure
-- that computes and store the average score of a student
-- an average score can be a decimal
-- procedure is taking 1 input and is linking to an existing users
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    DECLARE average_score DECIMAL (10, 2);
    SELECT AVG(score) INTO average_score FROM corrections WHERE user_id = user_id;
    UPDATE users SET average_score = CASE WHEN average_score > 0 THEN average_score
    ELSE 0 END WHERE id = user_id;
END $$
DELIMITER ;
