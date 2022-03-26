-- 给特定用户定义权限

Alter user 'user1'@'%' IDENTIFIED WITH mysql_native_password BY '1231234';
GRANT ALL PRIVILEGES ON myproject.* TO 'user1'@'%';
FLUSH PRIVILEGES;