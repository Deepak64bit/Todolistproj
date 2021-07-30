DROP TABLE IF EXISTS TASKTABLE;

CREATE TABLE TASKTABLE (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       taskname TEXT NOT NULL,
       creation DATETIME,
       due DATETIME NOT NULL,
       details TEXT,
       progress TEXT
       );    