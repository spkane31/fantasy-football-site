-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS matchups;
DROP TABLE IF EXISTS drafts;

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

CREATE TABLE drafts (
    id INTEGER NOT NULL,
    year INTEGER,
    pick_number INTEGER,
    player VARCHAR(64),
    player_id VARCHAR(64),
    round INTEGER,
    round_pick INTEGER,
    team VARCHAR(64),
    PRIMARY KEY (id)
)