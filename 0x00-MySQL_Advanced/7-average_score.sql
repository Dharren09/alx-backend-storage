-- script creates a stored procedure
-- that computes and store the average score of a student
-- an average score can be a decimal
-- procedure is taking 1 input and is linking to an existing users
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DROP TABLE IF EXISTS average_scores;
    CREATE TABLE average_scores (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	average_score DECIMAL(10,2) NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    INSERT INTO average_scores (user_id, average_score)
    SELECT user_id, AVG(score)
    FROM corrections
    WHERE user_id = user_id
    GROUP BY user_id;
END $$
DELIMITER ;
