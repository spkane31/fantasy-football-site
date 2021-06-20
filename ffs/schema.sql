-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;

CREATE TABLE matchups (
	id INTEGER NOT NULL,
    year INTEGER,
    week INTEGER,
	winner VARCHAR(64),
	loser VARCHAR(64),
    winner_score DOUBLE PRECISION,
    loser_score DOUBLE PRECISION,
	PRIMARY KEY (id)
);