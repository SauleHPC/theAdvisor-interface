
## how to create user and database from root

log in as root mysql user
```
mysql -u root -p  
```

do user things
```
CREATE USER 'esaule'@'localhost' IDENTIFIED by 'MYAMAZINGPASSWORD';
CREATE DATABASE theAdvisorEsaule ;
GRANT ALL PRIVILEGES ON theAdvisorEsaule.* to 'esaule'@'localhost';
FLUSH PRIVILEGES;
```

## log in mysql

Suggest defining user credentials in `~/bin/mysql_creds` so that you can do

```
. ~/bin/mysql_creds
mysql --user $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
```
