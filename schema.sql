CREATE TABLE IF NOT EXISTS User (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email     STRING  UNIQUE,
    password  STRING  NOT NULL,
    firstName STRING,
    lastName  STRING
);