-- script that creates index on the table and the first letter of the name
-- import a dump
-- only first lettter of name must be indexed
CREATE INDEX idx_name_first ON names (name(1));
