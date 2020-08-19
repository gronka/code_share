-- CREATE DATABASE movies;

-- CREATE USER movie_admin WITH PASSWORD 'newpassword';
-- ALTER USER movie_admin WITH LOGIN;
-- GRANT ALL PRIVILEGES ON DATABASE movies TO movie_admin;

ALTER USER postgres WITH PASSWORD 'newpassword';

CREATE TABLE characters (
	char_uuid UUID NOT NULL,
	character_name TEXT,
	PRIMARY KEY (char_uuid)
);

CREATE TABLE films (
	film_uuid UUID NOT NULL,
	char_uuid UUID NOT NULL,
	title TEXT,
	PRIMARY KEY (film_uuid)
);

INSERT INTO characters (char_uuid, character_name) VALUES ( '00000000-0000-0000-0000-000000000001', 'Luke');
INSERT INTO characters (char_uuid, character_name) VALUES ( '00000000-0000-0000-0000-000000000002', 'Yoda');
