-- SQL query to check if a user exists in the database
SELECT COUNT(*) 
FROM users 
WHERE name = %(user_name)s;