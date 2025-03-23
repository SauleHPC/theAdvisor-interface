
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
GRANT SUPER ON *.* TO 'esaule'@'localhost';
GRANT SYSTEM_USER ON *.* TO 'esaule'@'localhost';
FLUSH PRIVILEGES;
```

I needed to add some stuff in `/etc/mysql/conf.d/mysql.cnf`

```
[mysqld]
sql_mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
```

## log in mysql

Suggest defining user credentials in `~/bin/mysql_creds` so that you can do

```
. ~/bin/mysql_creds
mysql --user $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
```


## import the tables

You may need to flush the tables from a previous run
```
echo 'DROP TABLE citations;  DROP TABLE paperVersions; DROP TABLE papers; DROP TABLE authors; ' | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE 
```

I needed to update the `versionTime` timestamp to default to `CURRENT_TIMESTAMP`

```
mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE < create_schema.sql
zcat csx_db_authors.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
zcat csx_db_papers.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
zcat csx_db_paperVersions.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
zcat csx_db_citations.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
```

note that the order matters

for reference authors took a couple minutes; papers took 4 minutes;  paperVersions took about a minute; citations took about 45 minutes.

note that citations creates an error at the end, not sure why. But the data seem to be there.