-- Create the main database
CREATE DATABASE IF NOT EXISTS f1_application;
USE f1_application;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Drivers Table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50),
    team VARCHAR(50)
);

-- Races Table
CREATE TABLE IF NOT EXISTS races (
    race_id INT AUTO_INCREMENT PRIMARY KEY,
    race_name VARCHAR(100) NOT NULL,
    race_date DATE NOT NULL
);

-- Race Results Table
-- Stores the actual positions of drivers after each race
CREATE TABLE IF NOT EXISTS race_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    race_id INT,
    driver_id INT,
    position INT NOT NULL,
    FOREIGN KEY (race_id) REFERENCES races(race_id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE
);

-- Guesses Table
-- Stores users' guesses for top 3 positions in each race
CREATE TABLE IF NOT EXISTS guesses (
    guess_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    race_id INT,
    position_1_driver_id INT,
    position_2_driver_id INT,
    position_3_driver_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (race_id) REFERENCES races(race_id) ON DELETE CASCADE,
    FOREIGN KEY (position_1_driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (position_2_driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (position_3_driver_id) REFERENCES drivers(driver_id)
);

-- Race Drivers Table
-- Associates drivers with races, indicating which drivers are eligible for each race
CREATE TABLE IF NOT EXISTS race_drivers (
    race_driver_id INT AUTO_INCREMENT PRIMARY KEY,
    race_id INT,
    driver_id INT,
    FOREIGN KEY (race_id) REFERENCES races(race_id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE
);