CREATE TABLE tripupdate_db
(
    trip_id TEXT NOT NULL,
    stop_sequence INT NOT NULL,
    stop_id TEXT NOT NULL,
    delay INT NULL,
    arrival_time DATETIME NOT NULL,
    updated_at DATETIME NULL
);

CREATE TABLE timetable_db
(
    trip_id TEXT NOT NULL,
    shape_id TEXT NOT NULL,
    tt TEXT NOT NULL
);