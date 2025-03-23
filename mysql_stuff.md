
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


## import the tables

You may need to flush the tables from a previous run
```
echo 'DROP TABLE authors; DROP TABLE papers; DROP TABLE paperVersions; DROP TABLE citations' | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE 
```

I needed to update the `versionTime` timestamp to default to `CURRENT_TIMESTAMP`

```
mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE < create_schema.sql
zcat csx_db_authors.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
zcat csx_db_papers.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
zcat csx_db_paperVersions.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
zcat csx_db_citations.sql.gz | mysql -u $MYSQL_USER --password="$MYSQL_PASSWORD" $MYSQL_DATABASE
```