CREATE DATABASE IF NOT EXISTS loveefy_db;
CREATE USER IF NOT EXISTS 'loveefy_developer'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON loveefy_db.* TO 'loveefy_developer'@'localhost';
FLUSH PRIVILEGES;
