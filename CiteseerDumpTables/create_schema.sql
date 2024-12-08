CREATE TABLE authors (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    Cluster BIGINT DEFAULT NULL,
    name VARCHAR(100) NOT NULL,
    affil VARCHAR(255) DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    ord INT DEFAULT NULL,
    paperid VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE papers (
    id VARCHAR(100) NOT NULL,
    version INT UNSIGNED NOT NULL,
    cluster BIGINT UNSIGNED DEFAULT NULL,
    title VARCHAR(255) DEFAULT NULL,
    abstract TEXT DEFAULT NULL,
    year INT DEFAULT NULL,
    venue VARCHAR(255) DEFAULT NULL,
    venueType VARCHAR(20) DEFAULT NULL,
    pages VARCHAR(20) DEFAULT NULL,
    volume INT DEFAULT NULL,
    number INT DEFAULT NULL,
    publisher VARCHAR(100) DEFAULT NULL,
    pubAddress VARCHAR(100) DEFAULT NULL,
    tech VARCHAR(100) DEFAULT NULL,
    public TINYINT NOT NULL DEFAULT 1,
    ncites INT UNSIGNED NOT NULL DEFAULT 0,
    versionName VARCHAR(20) DEFAULT NULL,
    crawlDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    repositoryID VARCHAR(15) DEFAULT NULL,
    conversionTrace VARCHAR(255) DEFAULT NULL,
    selfCites INT UNSIGNED NOT NULL DEFAULT 0,
    versionTime TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (id)
);
CREATE TABLE paperVersions (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) DEFAULT NULL,
    paperid VARCHAR(100) NOT NULL,
    version INT DEFAULT NULL,
    repositoryID VARCHAR(15) NOT NULL,
    path VARCHAR(255) NOT NULL,
    deprecated TINYINT NOT NULL DEFAULT 0,
    spam TINYINT NOT NULL DEFAULT 0,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
CREATE TABLE `citations` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cluster` bigint(20) unsigned DEFAULT NULL,
  `authors` text,
  `title` varchar(255) DEFAULT NULL,
  `venue` varchar(255) DEFAULT NULL,
  `venueType` varchar(20) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `pages` varchar(20) DEFAULT NULL,
  `editors` text,
  `publisher` varchar(100) DEFAULT NULL,
  `pubAddress` varchar(100) DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `tech` varchar(100) DEFAULT NULL,
  `raw` text,
  `paperid` varchar(100) NOT NULL,
  `self` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86941372 DEFAULT CHARSET=utf8;
