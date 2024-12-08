CREATE DATABASE IF NOT EXISTS counter_db;
USE counter_db;

CREATE TABLE IF NOT EXISTS table_Counter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datetime DATETIME NOT NULL,
    client_info TEXT NOT NULL
);
