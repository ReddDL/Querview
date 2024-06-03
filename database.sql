-- DE LEON, Richard Emmanuel 
-- GALIDO, Alyanna Nicole
-- LEONCIO, Kathleen Kate
-- REYES, Mark Andrei 
-- CMSC 127 S7l 
-- Project milestone 3

DROP DATABASE IF EXISTS 127Project;
CREATE DATABASE IF NOT EXISTS 127Project;
USE 127Project;

-- MariaDB dump 10.19-11.3.2-MariaDB, for osx10.19 (arm64)
--
-- Host: localhost    Database: 127ProjectV2
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `food_establishment`
--

DROP TABLE IF EXISTS `food_establishment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `food_establishment` (
  `foodEst_id` int(7) NOT NULL AUTO_INCREMENT,
  `foodEst_name` varchar(50) NOT NULL,
  `foodEst_loc` varchar(50) NOT NULL,
  `foodEst_type` enum('Restaurant','Cafe','Fast Food','Other') NOT NULL,
  `foodEst_rating` double DEFAULT NULL,
  PRIMARY KEY (`foodEst_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_establishment`
--

LOCK TABLES `food_establishment` WRITE;
/*!40000 ALTER TABLE `food_establishment` DISABLE KEYS */;
INSERT INTO `food_establishment` VALUES
(1,'Tasty Bites','123 Main Street','Restaurant',5),
(2,'Spice Garden','456 Elm Street','Cafe',3),
(3,'Pizza Palace','789 Oak Street','Fast Food',3);
/*!40000 ALTER TABLE `food_establishment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food_item`
--

DROP TABLE IF EXISTS `food_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `food_item` (
  `foodItem_id` int(7) NOT NULL AUTO_INCREMENT,
  `foodItem_name` varchar(50) NOT NULL,
  `foodItem_price` decimal(6,2) NOT NULL,
  `foodItem_type` enum('Meat','Fruit','Vegetable','Staple','Dessert','Appetizer','Dairy','Seafood','Beverage','Soup') NOT NULL,
  `foodItem_desc` varchar(100) NOT NULL,
  `foodItem_rating` double DEFAULT NULL,
  `foodEst_id` int(7) DEFAULT NULL,
  PRIMARY KEY (`foodItem_id`),
  KEY `food_item_foodEst_id_Fk` (`foodEst_id`),
  CONSTRAINT `food_item_foodEst_id_Fk` FOREIGN KEY (`foodEst_id`) REFERENCES `food_establishment` (`foodEst_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_item`
--

LOCK TABLES `food_item` WRITE;
/*!40000 ALTER TABLE `food_item` DISABLE KEYS */;
INSERT INTO `food_item` VALUES
(1,'Cheeseburger',9.99,'Staple','A classic cheeseburger with lettuce, tomato, and pickles.',5,1),
(2,'Margherita Pizza',12.99,'Staple','Traditional pizza topped with tomato sauce, fresh mozzarella, and basil.',4,2),
(3,'Chicken Caesar Salad',8.49,'Vegetable','Fresh romaine lettuce topped with grilled chicken, croutons, and Caesar dressing.',5,1),
(4,'Pad Thai',10.99,'Staple','Stir-fried rice noodles with tofu, bean sprouts, peanuts, and a tangy sauce.',3,2),
(5,'Sushi Combo',15.99,'Staple','Assorted sushi rolls including tuna, salmon, and California rolls.',5,3),
(6,'Grilled Salmon',16.99,'Seafood','Fresh Atlantic salmon grilled to perfection served with steamed vegetables.',2,3),
(7,'Chicken Tikka Masala',13.99,'Meat','Tender chicken pieces cooked in a creamy tomato sauce with Indian spices.',3,1),
(8,'Pho Soup',11.49,'Soup','Traditional Vietnamese soup with rice noodles, beef broth, and herbs.',4,2),
(9,'Pasta Carbonara',14.99,'Staple','Spaghetti pasta with creamy egg sauce, pancetta, and Parmesan cheese.',5,3),
(10,'Falafel Wrap',7.99,'Staple','Falafel balls wrapped in pita bread with lettuce, tomato, and tahini sauce.',3,2);
/*!40000 ALTER TABLE `food_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review` (
  `review_id` int(7) NOT NULL AUTO_INCREMENT,
  `review_date` date NOT NULL,
  `content` varchar(100) NOT NULL,
  `rating` int(1) DEFAULT NULL,
  `userid` int(7) DEFAULT NULL,
  `foodEst_id` int(7) DEFAULT NULL,
  `foodItem_id` int(7) DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `review_userid_fk` (`userid`),
  KEY `review_foodEstid_fk` (`foodEst_id`),
  KEY `review_foodItemid_fk` (`foodItem_id`),
  CONSTRAINT `review_foodEstid_fk` FOREIGN KEY (`foodEst_id`) REFERENCES `food_establishment` (`foodEst_id`),
  CONSTRAINT `review_foodItemid_fk` FOREIGN KEY (`foodItem_id`) REFERENCES `food_item` (`foodItem_id`),
  CONSTRAINT `review_userid_fk` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES
(2,'2024-05-02','Margherita Pizza was delicious.',4,2,NULL,2),
(3,'2024-05-03','Enjoyed the Chicken Caesar Salad.',5,3,NULL,3),
(4,'2024-05-04','Pad Thai was too spicy for my taste.',3,1,NULL,4),
(5,'2024-05-05','Sushi Combo was fresh and tasty.',5,2,NULL,5),
(6,'2024-05-06','Grilled Salmon was overcooked.',2,3,NULL,6),
(7,'2024-05-07','Chicken Tikka Masala was too creamy.',3,1,NULL,7),
(8,'2024-05-08','Pho Soup was very comforting.',4,2,NULL,8),
(9,'2024-05-09','Loved the Pasta Carbonara.',5,3,NULL,9),
(10,'2024-05-10','Falafel Wrap was a bit dry.',3,1,NULL,10),
(11,'2024-05-11','Great restaurant with excellent service.',5,2,1,NULL),
(12,'2024-05-12','Lovely ambiance but the food was average.',3,3,2,NULL),
(13,'2024-05-13','Fast food place with quick service.',4,1,3,NULL),
(14,'2024-05-13','Fast food place with slow service.',3,1,3,NULL),
(15,'2024-05-13','Fast food place with pwede na service.',2,1,3,NULL),
(16,'2024-04-11','Love it.',5,2,1,NULL),
(17,'2024-03-06','Love it.',5,2,1,NULL),
(18,'2024-05-23','Its okay',3,1,1,NULL),
(19,'2024-05-23','its middle',3,1,NULL,1),
(20,'2024-05-23','its okay',3,1,NULL,1),
(21,'2024-05-23','its meow',2,1,NULL,1),
(22,'2024-05-23','its okay',3,1,NULL,1),
(23,'2024-05-23','test rev',3,1,NULL,1),
(24,'2024-05-23','test update',4,1,NULL,1);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_foodest`
--

DROP TABLE IF EXISTS `reviews_foodest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews_foodest` (
  `foodEst_id` int(7) NOT NULL,
  `review_id` int(7) NOT NULL,
  PRIMARY KEY (`foodEst_id`,`review_id`),
  KEY `reviewsFoodEst_reviewId_fk` (`review_id`),
  CONSTRAINT `reviewsFoodEst_foodEstId_fk` FOREIGN KEY (`foodEst_id`) REFERENCES `food_establishment` (`foodEst_id`),
  CONSTRAINT `reviewsFoodEst_reviewId_fk` FOREIGN KEY (`review_id`) REFERENCES `review` (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_foodest`
--

LOCK TABLES `reviews_foodest` WRITE;
/*!40000 ALTER TABLE `reviews_foodest` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_foodest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_fooditem`
--

DROP TABLE IF EXISTS `reviews_fooditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews_fooditem` (
  `userid` int(7) NOT NULL,
  `foodItem_id` int(7) NOT NULL,
  PRIMARY KEY (`userid`,`foodItem_id`),
  KEY `reviewsFoodItem_foodItemId_fk` (`foodItem_id`),
  CONSTRAINT `reviewsFoodItem_foodItemId_fk` FOREIGN KEY (`foodItem_id`) REFERENCES `food_item` (`foodItem_id`),
  CONSTRAINT `reviewsFoodItem_userid_fk` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_fooditem`
--

LOCK TABLES `reviews_fooditem` WRITE;
/*!40000 ALTER TABLE `reviews_fooditem` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_fooditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serves`
--

DROP TABLE IF EXISTS `serves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serves` (
  `foodEst_id` int(7) NOT NULL,
  `foodItem_id` int(7) NOT NULL,
  PRIMARY KEY (`foodEst_id`,`foodItem_id`),
  KEY `serves_foodItemId_fk` (`foodItem_id`),
  CONSTRAINT `serves_foodEstId_fk` FOREIGN KEY (`foodEst_id`) REFERENCES `food_establishment` (`foodEst_id`),
  CONSTRAINT `serves_foodItemId_fk` FOREIGN KEY (`foodItem_id`) REFERENCES `food_item` (`foodItem_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serves`
--

LOCK TABLES `serves` WRITE;
/*!40000 ALTER TABLE `serves` DISABLE KEYS */;
INSERT INTO `serves` VALUES
(1,1),
(2,2),
(1,3),
(2,4),
(3,5),
(3,6),
(1,7),
(2,8),
(3,9),
(2,10);
/*!40000 ALTER TABLE `serves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userid` int(7) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `userpassword` longtext NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'john_doe','password123'),
(2,'jane_smith','securepass'),
(3,'mike_jackson','p@ssw0rd!'),
(4,'sara_williams','qwerty123'),
(5,'chris_brown','letmein');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26 21:13:21
