-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;

CREATE TABLE matchups (
	id INTEGER NOT NULL,
    year INTEGER,
    week INTEGER,
	home_team VARCHAR(64),
	away_team VARCHAR(64),
    home_score DOUBLE PRECISION,
    away_score DOUBLE PRECISION,
	PRIMARY KEY (id)
);