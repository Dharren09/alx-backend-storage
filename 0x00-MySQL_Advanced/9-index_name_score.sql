-- script that creates an index on the table names
-- firsst letter of name and the score
-- imports a table dump
-- only the first letter of name and score must be indexed
CREATE INDEX idx_name_first_score
ON names (name(1), score);
