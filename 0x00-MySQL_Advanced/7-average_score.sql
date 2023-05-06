-- script creates a stored procedure
-- that computes and store the average score of a student
-- an average score can be a decimal
-- procedure is taking 1 input and is linking to an existing users
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    UPDATE users
    SET average_score = (
	SELECT AVG(score)
        FROM corrections
        WHERE user_id = user_id
    )
    WHERE id = user_id;
END $$
DELIMITER ;
