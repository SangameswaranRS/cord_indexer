create schema cv19;
use cv19;
CREATE TABLE `cv19`.`indexToResultCounts` (
  `docId` VARCHAR(50) NOT NULL,
  `paperTitle` VARCHAR(1000) NOT NULL,
  `paperAbstract` VARCHAR(5000) NOT NULL,
  `paperUrl` VARCHAR(1000) NOT NULL,
  `count` INT NOT NULL,
  PRIMARY KEY (`docId`),
  UNIQUE INDEX `docId_UNIQUE` (`docId` ASC));
