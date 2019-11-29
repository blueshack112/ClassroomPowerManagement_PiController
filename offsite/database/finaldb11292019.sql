-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: db_classroom_management
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
-- Table structure for table `tbl_courses`
--

DROP TABLE IF EXISTS `tbl_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_courses` (
  `course_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `course_credit_hours` int(11) NOT NULL,
  `total_students_enrolled` int(11) NOT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `course_id_UNIQUE` (`course_id`),
  KEY `teacher_id_idx` (`teacher_id`),
  CONSTRAINT `teacher_courses` FOREIGN KEY (`teacher_id`) REFERENCES `tbl_teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_courses`
--

LOCK TABLES `tbl_courses` WRITE;
/*!40000 ALTER TABLE `tbl_courses` DISABLE KEYS */;
INSERT INTO `tbl_courses` VALUES (1001,1001,'Basic Electronics',2,27),(1002,1001,'Functonal English',2,46),(1003,1001,'Pakistan Studies',2,54),(1004,1001,'Islamic Studies',2,43),(1005,1002,'Numerical Computing',3,27),(1006,1002,'Compiler Construction',3,44),(1007,1002,'Marketing and Management',3,55),(1008,1002,'Discrete Structure',3,33),(1009,1002,'Objecct Oriented Programming',3,45),(1010,1002,'Operating System',3,42),(1011,1003,'Software Project Management',3,23),(1012,1003,'Financial Management',3,31);
/*!40000 ALTER TABLE `tbl_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_debug`
--

DROP TABLE IF EXISTS `tbl_debug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_debug` (
  `debug_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_date_time_to_set` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`debug_id`),
  UNIQUE KEY `debug_id_UNIQUE` (`debug_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='for debugging purposes only. no affect on the software whatsoever.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_debug`
--

LOCK TABLES `tbl_debug` WRITE;
/*!40000 ALTER TABLE `tbl_debug` DISABLE KEYS */;
INSERT INTO `tbl_debug` VALUES (1,'2019-11-04 08:30:00');
/*!40000 ALTER TABLE `tbl_debug` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_extra_schedule`
--

DROP TABLE IF EXISTS `tbl_extra_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_extra_schedule` (
  `extra_schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `accept_status` varchar(45) NOT NULL,
  `request_type` varchar(45) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `day_of_week` int(11) DEFAULT NULL,
  `slot` int(11) DEFAULT NULL,
  `class_length` int(11) DEFAULT NULL,
  `week_schedule_id` int(11) DEFAULT NULL,
  `general_reason` text,
  `message` text,
  PRIMARY KEY (`extra_schedule_id`),
  UNIQUE KEY `extra_schedule_id_UNIQUE` (`extra_schedule_id`),
  KEY `extra_course_fkey_idx` (`course_id`),
  KEY `extra_room_id_idx` (`room_id`),
  KEY `extra__normal_schedule_fkey_idx` (`week_schedule_id`),
  CONSTRAINT `extra__normal_schedule_fkey` FOREIGN KEY (`week_schedule_id`) REFERENCES `tbl_week_schedule` (`week_schedule_id`),
  CONSTRAINT `extra_course_fkey` FOREIGN KEY (`course_id`) REFERENCES `tbl_courses` (`course_id`),
  CONSTRAINT `extra_room_fkey` FOREIGN KEY (`room_id`) REFERENCES `tbl_rooms` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='to store info about extra_classes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_extra_schedule`
--

LOCK TABLES `tbl_extra_schedule` WRITE;
/*!40000 ALTER TABLE `tbl_extra_schedule` DISABLE KEYS */;
INSERT INTO `tbl_extra_schedule` VALUES (1,'NOT_ACCEPTED','EXTRA',1001,1001,5,2,1,NULL,'chup kar',NULL);
/*!40000 ALTER TABLE `tbl_extra_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_history`
--

DROP TABLE IF EXISTS `tbl_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_history` (
  `date` date NOT NULL,
  `room_id` int(11) NOT NULL,
  `slot` int(11) NOT NULL,
  `credit_hour` int(11) NOT NULL,
  `relay_used` int(11) NOT NULL,
  KEY `room_id_idx` (`room_id`),
  CONSTRAINT `room_history` FOREIGN KEY (`room_id`) REFERENCES `tbl_rooms` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_history`
--

LOCK TABLES `tbl_history` WRITE;
/*!40000 ALTER TABLE `tbl_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_login_accounts`
--

DROP TABLE IF EXISTS `tbl_login_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_login_accounts` (
  `account_id` int(11) NOT NULL,
  `permission_level` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email_address` varchar(100) DEFAULT NULL,
  UNIQUE KEY `account_id_UNIQUE` (`account_id`),
  KEY `account_id_idx` (`account_id`),
  CONSTRAINT `account_teacher` FOREIGN KEY (`account_id`) REFERENCES `tbl_teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_login_accounts`
--

LOCK TABLES `tbl_login_accounts` WRITE;
/*!40000 ALTER TABLE `tbl_login_accounts` DISABLE KEYS */;
INSERT INTO `tbl_login_accounts` VALUES (1001,'Teacher','Hamdard123','ahmed.hassan.112.ha@gmail.com'),(1002,'Teacher','Hamdard123',NULL),(1003,'Teacher','Hamdard123',NULL),(1004,'Teacher','Hamdard123',NULL),(1005,'Teacher','Hamdard123',NULL),(1006,'Teacher','Hamdard123',NULL),(1007,'Teacher','Hamdard123',NULL),(1008,'Teacher','Hamdard123',NULL),(1009,'Teacher','Hamdard123',NULL),(1010,'Teacher','Hamdard123',NULL),(1011,'Teacher','Hamdard123',NULL),(1012,'HOD','HamdardHOD123',NULL),(1013,'Teacher','Hamdard123',NULL),(1014,'Teacher','Hamdard123',NULL),(1015,'QMD','HamdardQMD123',NULL);
/*!40000 ALTER TABLE `tbl_login_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_relays`
--

DROP TABLE IF EXISTS `tbl_relays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_relays` (
  `relay_id` int(11) NOT NULL,
  `no_of_associated_lights` int(11) NOT NULL,
  `no_of_assiocuated_fans` int(11) NOT NULL,
  `no_of_assiocuated_acs` int(11) NOT NULL,
  PRIMARY KEY (`relay_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_relays`
--

LOCK TABLES `tbl_relays` WRITE;
/*!40000 ALTER TABLE `tbl_relays` DISABLE KEYS */;
INSERT INTO `tbl_relays` VALUES (101,3,3,1),(102,0,0,1),(103,4,4,0),(104,4,4,0),(105,4,4,0),(106,4,4,0);
/*!40000 ALTER TABLE `tbl_relays` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_room_status`
--

DROP TABLE IF EXISTS `tbl_room_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_room_status` (
  `room_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `relay_used` varchar(255) NOT NULL,
  `attendance` int(11) NOT NULL,
  `class_date` date NOT NULL,
  `slot` int(11) NOT NULL,
  PRIMARY KEY (`room_id`,`course_id`),
  UNIQUE KEY `room_id_UNIQUE` (`room_id`),
  UNIQUE KEY `course_id_UNIQUE` (`course_id`),
  KEY `courses_idx` (`course_id`),
  CONSTRAINT `courses_roomstatus` FOREIGN KEY (`course_id`) REFERENCES `tbl_courses` (`course_id`),
  CONSTRAINT `room_roomstatus` FOREIGN KEY (`room_id`) REFERENCES `tbl_rooms` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_room_status`
--

LOCK TABLES `tbl_room_status` WRITE;
/*!40000 ALTER TABLE `tbl_room_status` DISABLE KEYS */;
INSERT INTO `tbl_room_status` VALUES (1001,1001,'101102103',55,'2019-06-03',1);
/*!40000 ALTER TABLE `tbl_room_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_rooms`
--

DROP TABLE IF EXISTS `tbl_rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_rooms` (
  `room_id` int(11) NOT NULL,
  `capacity` int(11) NOT NULL,
  `no_of_lights` int(11) NOT NULL,
  `no_of_fans` int(11) NOT NULL,
  `no_of_ac` int(11) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_rooms`
--

LOCK TABLES `tbl_rooms` WRITE;
/*!40000 ALTER TABLE `tbl_rooms` DISABLE KEYS */;
INSERT INTO `tbl_rooms` VALUES (1001,60,14,9,2),(1002,60,14,9,2),(1003,60,14,9,2),(1004,60,14,9,2),(1005,60,14,9,2),(1006,60,14,9,2),(1007,30,7,4,0),(1008,30,7,4,0),(1009,60,14,9,2),(1010,60,14,9,2),(1011,30,7,4,0),(1012,30,7,4,0),(1013,60,14,9,2),(1014,60,14,9,2),(1015,60,14,9,2);
/*!40000 ALTER TABLE `tbl_rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_schedule`
--

DROP TABLE IF EXISTS `tbl_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_schedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `slot` int(11) NOT NULL,
  `day_of_week` int(11) NOT NULL,
  `class_length` int(11) NOT NULL,
  PRIMARY KEY (`schedule_id`),
  UNIQUE KEY `schedule_id_UNIQUE` (`schedule_id`),
  KEY `course_id_idx` (`course_id`),
  KEY `room_schedule` (`room_id`),
  CONSTRAINT `course_schedule` FOREIGN KEY (`course_id`) REFERENCES `tbl_courses` (`course_id`),
  CONSTRAINT `room_schedule` FOREIGN KEY (`room_id`) REFERENCES `tbl_rooms` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_schedule`
--

LOCK TABLES `tbl_schedule` WRITE;
/*!40000 ALTER TABLE `tbl_schedule` DISABLE KEYS */;
INSERT INTO `tbl_schedule` VALUES (1,1001,1001,1,1,2),(2,1001,1002,3,1,2),(3,1001,1003,5,1,2),(4,1001,1004,1,2,2),(5,1001,1005,7,1,1),(6,1001,1005,3,2,2),(7,1001,1006,7,3,1),(8,1001,1006,5,2,2),(9,1001,1007,7,2,1),(10,1001,1007,1,3,2),(11,1001,1008,7,4,1),(12,1001,1008,3,3,2),(13,1001,1009,1,5,1),(14,1001,1009,5,3,2),(15,1001,1010,2,5,1),(16,1001,1010,1,4,2),(17,1001,1011,3,5,1),(18,1001,1011,3,4,2),(19,1001,1012,4,5,1),(20,1001,1012,5,4,2);
/*!40000 ALTER TABLE `tbl_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_teachers`
--

DROP TABLE IF EXISTS `tbl_teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_teachers` (
  `teacher_id` int(11) NOT NULL,
  `teacher_first_name` varchar(45) NOT NULL,
  `teacher_last_name` varchar(45) DEFAULT NULL,
  `teacher_designation` varchar(45) NOT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `idtbl_teachesr_UNIQUE` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_teachers`
--

LOCK TABLES `tbl_teachers` WRITE;
/*!40000 ALTER TABLE `tbl_teachers` DISABLE KEYS */;
INSERT INTO `tbl_teachers` VALUES (1001,'Shafaq','Sohail','asst_prof'),(1002,'Afzal','Hussain','asst_prof'),(1003,'Iqbaluddin','Khan','asst_prof'),(1004,'Adnan','Jaffri','asst_prof'),(1005,'Shams ul','Arfeen','asst_prof'),(1006,'Salman','Shah','asst_prof'),(1007,'Kamil','Sidiqui','asst_prof'),(1008,'Adeel','Mannan','asst_prof'),(1009,'Imran','Khan','asst_prof'),(1010,'Zafar','Ahmed','asst_prof'),(1011,'Noman','Siddiqui','asst_prof'),(1012,'Aqeel','Ur Rehman','HOD'),(1013,'Adnan','Ahmed','asst_prof'),(1014,'Asad','Ur Rehman','asst_prof'),(1015,'Suboohi','Mahmood','asst_prof');
/*!40000 ALTER TABLE `tbl_teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_week_schedule`
--

DROP TABLE IF EXISTS `tbl_week_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tbl_week_schedule` (
  `week_schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `schedule_id` int(11) DEFAULT NULL,
  `extra_schedule_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`week_schedule_id`),
  UNIQUE KEY `week_sched_id_UNIQUE` (`week_schedule_id`),
  UNIQUE KEY `schedule_id_UNIQUE` (`schedule_id`),
  UNIQUE KEY `extra_scheule_id_UNIQUE` (`extra_schedule_id`),
  CONSTRAINT `extra_schedule_fkey` FOREIGN KEY (`extra_schedule_id`) REFERENCES `tbl_extra_schedule` (`extra_schedule_id`),
  CONSTRAINT `schedule_fkey` FOREIGN KEY (`schedule_id`) REFERENCES `tbl_schedule` (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='For current week''s schedule';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_week_schedule`
--

LOCK TABLES `tbl_week_schedule` WRITE;
/*!40000 ALTER TABLE `tbl_week_schedule` DISABLE KEYS */;
INSERT INTO `tbl_week_schedule` VALUES (1,1,NULL),(2,NULL,1);
/*!40000 ALTER TABLE `tbl_week_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `view_extra_schedule`
--

DROP TABLE IF EXISTS `view_extra_schedule`;
/*!50001 DROP VIEW IF EXISTS `view_extra_schedule`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `view_extra_schedule` AS SELECT 
 1 AS `extra_schedule_id`,
 1 AS `room_id`,
 1 AS `course_id`,
 1 AS `slot`,
 1 AS `day_of_week`,
 1 AS `class_length`,
 1 AS `accept_status`,
 1 AS `teacher_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_normal_schedule`
--

DROP TABLE IF EXISTS `view_normal_schedule`;
/*!50001 DROP VIEW IF EXISTS `view_normal_schedule`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `view_normal_schedule` AS SELECT 
 1 AS `schedule_id`,
 1 AS `room_id`,
 1 AS `course_id`,
 1 AS `slot`,
 1 AS `day_of_week`,
 1 AS `class_length`,
 1 AS `teacher_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_room_status`
--

DROP TABLE IF EXISTS `view_room_status`;
/*!50001 DROP VIEW IF EXISTS `view_room_status`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `view_room_status` AS SELECT 
 1 AS `class_date`,
 1 AS `room_id`,
 1 AS `course_id`,
 1 AS `course_name`,
 1 AS `teacher_first_name`,
 1 AS `teacher_last_name`,
 1 AS `class_length`,
 1 AS `attendance`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_teacher_schedule`
--

DROP TABLE IF EXISTS `view_teacher_schedule`;
/*!50001 DROP VIEW IF EXISTS `view_teacher_schedule`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `view_teacher_schedule` AS SELECT 
 1 AS `course_name`,
 1 AS `teacher_id`,
 1 AS `room_id`,
 1 AS `course_id`,
 1 AS `day_of_week`,
 1 AS `slot`,
 1 AS `class_length`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'db_classroom_management'
--

--
-- Dumping routines for database 'db_classroom_management'
--

--
-- Final view structure for view `view_extra_schedule`
--

/*!50001 DROP VIEW IF EXISTS `view_extra_schedule`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_extra_schedule` AS select `tbl_week_schedule`.`extra_schedule_id` AS `extra_schedule_id`,`tbl_extra_schedule`.`room_id` AS `room_id`,`tbl_extra_schedule`.`course_id` AS `course_id`,`tbl_extra_schedule`.`slot` AS `slot`,`tbl_extra_schedule`.`day_of_week` AS `day_of_week`,`tbl_extra_schedule`.`class_length` AS `class_length`,`tbl_extra_schedule`.`accept_status` AS `accept_status`,`tbl_courses`.`teacher_id` AS `teacher_id` from ((`tbl_week_schedule` left join `tbl_extra_schedule` on((`tbl_week_schedule`.`extra_schedule_id` = `tbl_extra_schedule`.`extra_schedule_id`))) left join `tbl_courses` on((`tbl_extra_schedule`.`course_id` = `tbl_courses`.`course_id`))) where (`tbl_extra_schedule`.`accept_status` = 'ACCEPTED') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_normal_schedule`
--

/*!50001 DROP VIEW IF EXISTS `view_normal_schedule`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_normal_schedule` AS select `tbl_week_schedule`.`schedule_id` AS `schedule_id`,`tbl_schedule`.`room_id` AS `room_id`,`tbl_schedule`.`course_id` AS `course_id`,`tbl_schedule`.`slot` AS `slot`,`tbl_schedule`.`day_of_week` AS `day_of_week`,`tbl_schedule`.`class_length` AS `class_length`,`tbl_courses`.`teacher_id` AS `teacher_id` from ((`tbl_week_schedule` left join `tbl_schedule` on((`tbl_week_schedule`.`schedule_id` = `tbl_schedule`.`schedule_id`))) left join `tbl_courses` on((`tbl_schedule`.`course_id` = `tbl_courses`.`course_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_room_status`
--

/*!50001 DROP VIEW IF EXISTS `view_room_status`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_room_status` AS select `tbl_room_status`.`class_date` AS `class_date`,`tbl_room_status`.`room_id` AS `room_id`,`tbl_courses`.`course_id` AS `course_id`,`tbl_courses`.`course_name` AS `course_name`,`tbl_teachers`.`teacher_first_name` AS `teacher_first_name`,`tbl_teachers`.`teacher_last_name` AS `teacher_last_name`,`tbl_schedule`.`class_length` AS `class_length`,`tbl_room_status`.`attendance` AS `attendance` from (((`tbl_room_status` left join `tbl_courses` on((`tbl_room_status`.`course_id` = `tbl_courses`.`course_id`))) left join `tbl_teachers` on((`tbl_courses`.`teacher_id` = `tbl_teachers`.`teacher_id`))) left join `tbl_schedule` on((`tbl_courses`.`course_id` = `tbl_schedule`.`course_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_teacher_schedule`
--

/*!50001 DROP VIEW IF EXISTS `view_teacher_schedule`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_teacher_schedule` AS select `tbl_courses`.`course_name` AS `course_name`,`tbl_courses`.`teacher_id` AS `teacher_id`,`tbl_schedule`.`room_id` AS `room_id`,`tbl_schedule`.`course_id` AS `course_id`,`tbl_schedule`.`day_of_week` AS `day_of_week`,`tbl_schedule`.`slot` AS `slot`,`tbl_schedule`.`class_length` AS `class_length` from (`tbl_courses` left join `tbl_schedule` on((`tbl_courses`.`course_id` = `tbl_schedule`.`course_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-29 14:51:26
