CREATE DATABASE IF NOT EXISTS f1_application;
USE f1_application;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS races (
    race_id INT AUTO_INCREMENT PRIMARY KEY,
    race_name VARCHAR(100) NOT NULL,
    race_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS guesses (
    guess_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    race_id INT,
    position_1 VARCHAR(50),
    position_2 VARCHAR(50),
    position_3 VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (race_id) REFERENCES races(race_id)
);
