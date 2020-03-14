DROP TABLE IF EXISTS station;
DROP TABLE IF EXISTS measurements;


CREATE TABLE station(
	station VARCHAR(255),
	name VARCHAR(255) NOT NULL,
	latitude FLOAT,
	longitude FLOAT,
	elevation FLOAT NOT NULL,
	PRIMARY KEY (station)
);

DROP TABLE measurements;

SELECT * FROM measurements;
CREATE TABLE measurements(
	station VARCHAR(255) NOT NULL,
	date VARCHAR(255) NOT NULL,
	prcp FLOAT,
	tobs INT,
	primary key (station, date),
	CONSTRAINT FK_measurements FOREIGN KEY (station)
    REFERENCES station(station)
);

