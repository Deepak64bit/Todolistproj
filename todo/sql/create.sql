DROP TABLE IF EXISTS TASKTABLE;

CREATE TABLE TASKTABLE (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       taskname TEXT,
       creation DATETIME,
       due DATETIME,
       details TEXT,
       progress TEXT
       );    