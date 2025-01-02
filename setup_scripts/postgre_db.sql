-- Create the database
CREATE DATABASE loveefy_development_db;

-- Create the user with a password
DO
$$
BEGIN
   IF NOT EXISTS (
       SELECT FROM pg_catalog.pg_roles 
       WHERE rolname = 'loveefy_developer'
   ) THEN
       CREATE ROLE loveefy_developer WITH LOGIN PASSWORD '123456';
   END IF;
END
$$;

-- Grant privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE loveefy_development_db TO loveefy_developer;