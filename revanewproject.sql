-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: revanew
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tbl_accounts`
--

DROP TABLE IF EXISTS `tbl_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_accounts` (
  `account_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `account_user_id` bigint(20) NOT NULL,
  `account_name` varchar(45) NOT NULL,
  `account_amount` decimal(13,2) NOT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `account_name` (`account_name`),
  KEY `account_user_id` (`account_user_id`),
  CONSTRAINT `tbl_accounts_ibfk_1` FOREIGN KEY (`account_user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_accounts`
--

LOCK TABLES `tbl_accounts` WRITE;
/*!40000 ALTER TABLE `tbl_accounts` DISABLE KEYS */;
INSERT INTO `tbl_accounts` VALUES (1,1,'savings',3000.23),(2,2,'notsavings',45.23),(3,1,'checkings',4500.23),(4,1,'offshore account',1738.69),(5,1,'newZeelandAcc',69.00);
/*!40000 ALTER TABLE `tbl_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_deductions`
--

DROP TABLE IF EXISTS `tbl_deductions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_deductions` (
  `deduction_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `deduction_frequency` varchar(4) NOT NULL,
  `deduction_type` varchar(150) DEFAULT NULL,
  `deduction_amount` decimal(13,2) NOT NULL,
  `deduction_user_id` bigint(20) NOT NULL,
  `deduction_date` varchar(20) NOT NULL,
  `deduction_account` bigint(20) NOT NULL,
  PRIMARY KEY (`deduction_id`),
  KEY `deduction_user_id` (`deduction_user_id`),
  CONSTRAINT `tbl_deductions_ibfk_1` FOREIGN KEY (`deduction_user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_deductions`
--

LOCK TABLES `tbl_deductions` WRITE;
/*!40000 ALTER TABLE `tbl_deductions` DISABLE KEYS */;
INSERT INTO `tbl_deductions` VALUES (1,'30','Taxes',54.99,1,'20180801',1),(2,'30','Rent',600.00,1,'20180801',1);
/*!40000 ALTER TABLE `tbl_deductions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_expenses`
--

DROP TABLE IF EXISTS `tbl_expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_expenses` (
  `expense_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `expense_category` varchar(45) NOT NULL,
  `expense_cost` decimal(13,2) NOT NULL,
  `target_account` bigint(20) NOT NULL,
  `expense_processed` int(3) NOT NULL,
  `expense_date` varchar(12) NOT NULL,
  `expense_user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`expense_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_expenses`
--

LOCK TABLES `tbl_expenses` WRITE;
/*!40000 ALTER TABLE `tbl_expenses` DISABLE KEYS */;
INSERT INTO `tbl_expenses` VALUES (1,'groceries',55.45,1,0,'20190723',1),(2,'groceries',68.96,1,0,'20190624',1),(3,'groceries',12.11,1,0,'20190704',1),(4,'eating out',14.25,1,0,'20190805',1),(5,'eating out',23.25,1,0,'20190810',1);
/*!40000 ALTER TABLE `tbl_expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_incomes`
--

DROP TABLE IF EXISTS `tbl_incomes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_incomes` (
  `income_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `income_user_id` bigint(20) NOT NULL,
  `income_type` varchar(150) NOT NULL,
  `income_amount` decimal(13,2) NOT NULL,
  `income_date` varchar(20) NOT NULL,
  `income_frequency` varchar(4) NOT NULL,
  `income_account_id` bigint(20) NOT NULL,
  PRIMARY KEY (`income_id`),
  KEY `income_user_id` (`income_user_id`),
  CONSTRAINT `tbl_incomes_ibfk_1` FOREIGN KEY (`income_user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_incomes`
--

LOCK TABLES `tbl_incomes` WRITE;
/*!40000 ALTER TABLE `tbl_incomes` DISABLE KEYS */;
INSERT INTO `tbl_incomes` VALUES (2,1,'Work Work',600.23,'20190723','30',1),(3,1,'Work Work',600.23,'20190723','30',1),(4,1,'Work',4232.23,'20190704','23',1),(5,1,'BitCoin Mining',50000.00,'20190501','365',3),(6,1,'Sold Car',4500.00,'20190802','0',1);
/*!40000 ALTER TABLE `tbl_incomes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_save_for`
--

DROP TABLE IF EXISTS `tbl_save_for`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_save_for` (
  `sf_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sf_date` varchar(20) NOT NULL,
  `sf_desire` varchar(70) NOT NULL,
  `sf_cost` decimal(13,2) NOT NULL,
  `sf_user_id` bigint(20) NOT NULL,
  `sf_account` bigint(20) NOT NULL,
  `sf_start_date` varchar(20) NOT NULL,
  PRIMARY KEY (`sf_id`),
  KEY `sf_user_id` (`sf_user_id`),
  CONSTRAINT `tbl_save_for_ibfk_1` FOREIGN KEY (`sf_user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_save_for`
--

LOCK TABLES `tbl_save_for` WRITE;
/*!40000 ALTER TABLE `tbl_save_for` DISABLE KEYS */;
INSERT INTO `tbl_save_for` VALUES (3,'20191012','Vacation',100.00,1,1,'20190816');
/*!40000 ALTER TABLE `tbl_save_for` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_users`
--

DROP TABLE IF EXISTS `tbl_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_users` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_username` varchar(45) DEFAULT NULL,
  `user_password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_users`
--

LOCK TABLES `tbl_users` WRITE;
/*!40000 ALTER TABLE `tbl_users` DISABLE KEYS */;
INSERT INTO `tbl_users` VALUES (1,'blake','test@gmail.com','pbkdf2:sha256:150000$fO3wgOja$50adc05382e029b0e350e8978950a2774c53e7580e143f3c767e0f4d13419711'),(2,'blake411','test2@gmail.com','pbkdf2:sha256:150000$AL8F2I2D$5becf5f075397c3eb861936f8aef804b5c9d8415a224cc6cb21d6abc88612047'),(3,'blake411','test3@gmail.com','pbkdf2:sha256:150000$g8on44C9$9cdcccf7f4c0c723d93c9b0fe7691eac80ca6d03cf5f2ecd4aeb32db5010553b'),(4,'badfasdf','bert@bert','pbkdf2:sha256:150000$awyOJptl$169a20d632cf77f2465a67c13d59a6704988cb19023e1533830d73036b767fbd');
/*!40000 ALTER TABLE `tbl_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-17  0:48:14
