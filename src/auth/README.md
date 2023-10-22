## Explanation

What the authentication service does here is authenticate the user logging in to check if their credentials
are present in the database.

The `init.sql` initializes the `auth` database with a `user` table and inserts within it a customer user we created in that script.
Commands used:
- To initialize: mysql -u root -p < init.sql
- Access mysql: mysql -u root -p [and insert your password]
- show databases;
- show tables;