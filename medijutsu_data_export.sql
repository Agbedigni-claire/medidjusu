-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: medijutsu
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_admin` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_admin` (`email_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,' ','admin@gmail.com',NULL,'81dc9bdb52d04dc20036dbd8313ed055','2025-08-03 21:38:08');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admissions`
--

DROP TABLE IF EXISTS `admissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admissions` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `sexe` varchar(10) NOT NULL,
  `date_naissance` date NOT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `numero_assurance` varchar(50) DEFAULT NULL,
  `motif` varchar(255) NOT NULL,
  `date_admission` datetime DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `tension` varchar(20) DEFAULT NULL,
  `poids` float DEFAULT NULL,
  `observations` text,
  `pp_nom` varchar(100) DEFAULT NULL,
  `pp_prenom` varchar(100) DEFAULT NULL,
  `pp_telephone` varchar(20) DEFAULT NULL,
  `statut_sortie` varchar(100) DEFAULT 'non',
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admissions`
--

LOCK TABLES `admissions` WRITE;
/*!40000 ALTER TABLE `admissions` DISABLE KEYS */;
INSERT INTO `admissions` VALUES (7,'patient3','elodie','Femme','2025-08-14','lomer','123456','patient3@gmail.com','ojfoe','fiervre','2025-08-04 00:40:53',37,'120',252,'jjdif55','eloge','papa','12523685','oui'),(8,'eloge','patient','Homme','2025-08-03','telessous','+228 91271027','patient@gmail.com','','','2025-08-14 23:22:52',NULL,'',NULL,'','','','dddddd','oui'),(9,'papou','1235','Femme','2025-08-15',' placeholder=','+228 91271004','papapap@gmail.com','','','2025-08-14 23:26:41',NULL,'',NULL,'','','','','oui'),(10,'ddsdf','fdf','Femme','2025-08-06','dfd','dfdfd','sdsd@gmail.com','','dfdfd','2025-08-14 23:39:50',NULL,'fd',NULL,'','','','',NULL),(11,'papou','1235','Femme','2025-08-15',' placeholder=','+228 91271004','papapap@gmail.com','','','2025-08-14 23:45:03',NULL,'',NULL,'','zzzz','','','non'),(12,'patient','eloge','Homme','2065-08-03','telessous','+228 91271027','patient@gmail.com','','','2025-08-21 15:17:09',37,'35',65,'','','','','oui'),(13,'patient','eloge','Homme','2065-08-03','telessous','+228 91271027','patient@gmail.com','','','2025-08-21 17:57:40',37,'120',NULL,'','','','','oui'),(14,'GOMINA','patient 2','Homme','2025-08-14','None','+228 91271027','pateint4@gmail.coom','','','2025-08-21 18:07:44',NULL,'',NULL,'','','','','non'),(15,'patient','eloge','Homme','2065-08-03','telessous','+228 91271027','patient@gmail.com','','','2025-08-21 18:34:15',26,'180',11,'','','','','non'),(16,'patient','eloge','Homme','2065-08-03','telessous','+228 91271027','patient@gmail.com','15254','gros nez','2025-08-21 22:54:13',38,'120',900,'','','','','non'),(17,'kokou','padre','Femme','2044-08-11','','+228 47899556','kokou@gmail.com','','enceinte','2025-08-21 22:57:24',37,'120/80',45,'plokiksjndjf,f','eloge','papa','+228 97856258','non');
/*!40000 ALTER TABLE `admissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ambulancier`
--

DROP TABLE IF EXISTS `ambulancier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ambulancier` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_ambulancier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_ambulancier` (`email_ambulancier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ambulancier`
--

LOCK TABLES `ambulancier` WRITE;
/*!40000 ALTER TABLE `ambulancier` DISABLE KEYS */;
/*!40000 ALTER TABLE `ambulancier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caissier`
--

DROP TABLE IF EXISTS `caissier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `caissier` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_caissier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_caissier` (`email_caissier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caissier`
--

LOCK TABLES `caissier` WRITE;
/*!40000 ALTER TABLE `caissier` DISABLE KEYS */;
/*!40000 ALTER TABLE `caissier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultation`
--

DROP TABLE IF EXISTS `consultation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_consultation` datetime DEFAULT NULL,
  `date_confirmation` datetime DEFAULT NULL,
  `date_fin_consultation` datetime DEFAULT NULL,
  `consultation_precedente_id` int DEFAULT NULL,
  `consultation_suivante_id` int DEFAULT NULL,
  `etat` varchar(20) DEFAULT NULL,
  `motif` varchar(255) DEFAULT NULL,
  `plaintes` text,
  `antecedents_personnels` text,
  `antecedents_familiaux` text,
  `allergies` text,
  `traitements_en_cours` text,
  `poids` float DEFAULT NULL,
  `taille` float DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `tension_arterielle` varchar(10) DEFAULT NULL,
  `frequence_cardiaque` int DEFAULT NULL,
  `frequence_respiratoire` int DEFAULT NULL,
  `saturation_oxygene` float DEFAULT NULL,
  `observations_cliniques` text,
  `examens_biologiques` text,
  `examens_radiologiques` text,
  `autres_examens` text,
  `resultats_examens` text,
  `diagnostic` text,
  `diagnostic_secondaire` text,
  `traitement` text,
  `traitement_non_medic` text,
  `prescription` text,
  `conseils` text,
  `prochain_rdv` datetime DEFAULT NULL,
  `note_suivi` text,
  `ordonnance_jointe` varchar(255) DEFAULT NULL,
  `lettre_orientation` varchar(255) DEFAULT NULL,
  `documents_scannes` varchar(255) DEFAULT NULL,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consultation_precedente_id` (`consultation_precedente_id`),
  KEY `consultation_suivante_id` (`consultation_suivante_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `consultation_ibfk_1` FOREIGN KEY (`consultation_precedente_id`) REFERENCES `consultation` (`id`),
  CONSTRAINT `consultation_ibfk_2` FOREIGN KEY (`consultation_suivante_id`) REFERENCES `consultation` (`id`),
  CONSTRAINT `consultation_ibfk_3` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`ident`),
  CONSTRAINT `consultation_ibfk_4` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`ident`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultation`
--

LOCK TABLES `consultation` WRITE;
/*!40000 ALTER TABLE `consultation` DISABLE KEYS */;
INSERT INTO `consultation` VALUES (1,'2025-08-04 01:40:54','2025-08-04 01:40:54',NULL,NULL,2,'en_attente','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,'2025-08-04 01:40:54','2025-08-06 22:26:02'),(2,'2025-08-06 22:26:02','2025-08-06 22:28:56','2025-08-06 22:28:56',1,3,'Terminée','test','','','','','',NULL,NULL,NULL,'536',NULL,NULL,NULL,'','','','','','','','','','','','2025-08-17 00:00:00','','','','',1,1,'2025-08-06 22:26:02','2025-08-20 22:31:54'),(3,'2025-08-20 22:31:54','2025-08-20 22:31:54',NULL,2,6,'en_attente','papou',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,'2025-08-20 22:31:54','2025-08-21 18:51:40'),(6,'2025-08-21 18:51:40','2025-08-21 23:14:10','2025-08-21 23:14:10',3,7,'Terminée','mot de tete','ddf','','','','',11,NULL,26,'180',NULL,NULL,NULL,'','','','','','','','','','','fdfdf','2025-08-24 00:00:00','dfdsdvbr','','','',1,1,'2025-08-21 18:51:40','2025-08-21 23:14:10'),(7,'2025-08-21 23:02:42','2025-08-21 23:02:42',NULL,6,NULL,'en_attente','okijhyg',NULL,NULL,NULL,NULL,NULL,900,NULL,38,'120',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,3,'2025-08-21 23:02:42','2025-08-21 23:02:42'),(8,'2025-08-21 23:03:02','2025-08-21 23:03:02',NULL,NULL,NULL,'en_attente','',NULL,NULL,NULL,NULL,NULL,45,NULL,37,'120/80',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,9,1,'2025-08-21 23:03:02','2025-08-21 23:03:02');
/*!40000 ALTER TABLE `consultation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_doctor` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `groupe_sanguin` varchar(4) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `qualification` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `designation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_doctor` (`email_doctor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (1,'papi','docteur_eloge@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-03 21:39:17','docteur eloge',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'papatrou','docteur3@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-20 22:21:59','docteur3 papatrou','2025-08-17','Homme','Divorcé(e)','A-',NULL,NULL,'Agoè telessou','France','Lome','123456','+228 91271004','Diplôme d\'État de docteur en médecine','Infirmier / Infirmière',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'roc','pouwedeouroma@gmail.com','4fd04d6ba8e914c2f6130fab1c8c7161','2025-08-21 22:40:03','romaric p.','2025-08-07','Homme','Séparé(e)',NULL,'jp.jpg',NULL,'demakpouè','Togo',NULL,NULL,'+228 98524866','DES (Diplôme d\'Études Spécialisées)','Gynécologue','9','16','7','14','8','16','8','16','8',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gestionnaire_logistique`
--

DROP TABLE IF EXISTS `gestionnaire_logistique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestionnaire_logistique` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_logistique` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_logistique` (`email_logistique`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gestionnaire_logistique`
--

LOCK TABLES `gestionnaire_logistique` WRITE;
/*!40000 ALTER TABLE `gestionnaire_logistique` DISABLE KEYS */;
/*!40000 ALTER TABLE `gestionnaire_logistique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gestionnaire_stock`
--

DROP TABLE IF EXISTS `gestionnaire_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestionnaire_stock` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_stock` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_stock` (`email_stock`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gestionnaire_stock`
--

LOCK TABLES `gestionnaire_stock` WRITE;
/*!40000 ALTER TABLE `gestionnaire_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `gestionnaire_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infirmier`
--

DROP TABLE IF EXISTS `infirmier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `infirmier` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_infirmier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_infirmier` (`email_infirmier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infirmier`
--

LOCK TABLES `infirmier` WRITE;
/*!40000 ALTER TABLE `infirmier` DISABLE KEYS */;
/*!40000 ALTER TABLE `infirmier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interne_medecine`
--

DROP TABLE IF EXISTS `interne_medecine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interne_medecine` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_interne` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_interne` (`email_interne`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interne_medecine`
--

LOCK TABLES `interne_medecine` WRITE;
/*!40000 ALTER TABLE `interne_medecine` DISABLE KEYS */;
/*!40000 ALTER TABLE `interne_medecine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_patient` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `etat_civil` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profession` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `groupe_sanguin` varchar(4) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tension_arterielle` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `taux_sucre` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `derniere_connexion` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_patient` (`email_patient`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'papa','patient@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-03 21:40:09','patient eloge','2065-08-03','Homme','Célibataire','etudiant','B+','14','25',NULL,'telessous','Lome','Togo','123456','+228 91271027',1,NULL),(2,NULL,'patient2@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-03 23:13:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL),(3,NULL,'patient3@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-04 00:40:53','patient3 elodie','2025-08-14','Femme',NULL,NULL,NULL,NULL,NULL,NULL,'lomer',NULL,NULL,NULL,'123456',1,NULL),(4,NULL,'papapap@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-14 23:26:41','papou 1235','2025-08-15','Femme',NULL,NULL,NULL,NULL,NULL,NULL,' placeholder=',NULL,NULL,NULL,'+228 91271004',1,NULL),(6,NULL,'sdsd@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-14 23:39:50','ddsdf fdf','2025-08-06','Femme',NULL,NULL,NULL,NULL,NULL,NULL,'dfd',NULL,NULL,NULL,'dfdfd',1,NULL),(7,'plok','patient7@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-19 23:18:26','7 GOMINA','2034-08-24',NULL,NULL,'None',NULL,'None','None',NULL,'None','None',NULL,'None','+228 91271027',1,NULL),(8,'eric','pateint4@gmail.coom','81dc9bdb52d04dc20036dbd8313ed055','2025-08-20 22:24:31','GOMINA patient 2','2025-08-14',NULL,'Célibataire','None','A-','None','None',NULL,'None','None',NULL,'None','+228 91271027',1,NULL),(9,NULL,'kokou@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-21 22:57:24','kokou padre','2044-08-11','Femme',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,'+228 47899556',1,NULL);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produits`
--

DROP TABLE IF EXISTS `produits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produits` (
  `reference` varchar(100) NOT NULL,
  `nom_produit` varchar(225) DEFAULT NULL,
  `quantite` int DEFAULT NULL,
  PRIMARY KEY (`reference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produits`
--

LOCK TABLES `produits` WRITE;
/*!40000 ALTER TABLE `produits` DISABLE KEYS */;
/*!40000 ALTER TABLE `produits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rendezvous`
--

DROP TABLE IF EXISTS `rendezvous`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rendezvous` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int DEFAULT NULL,
  `secretaire_id` int DEFAULT NULL,
  `date_rdv` date NOT NULL,
  `heure_debut` time NOT NULL,
  `heure_fin` time NOT NULL,
  `statut` enum('en attente','confirmé','annulé','terminé') DEFAULT NULL,
  `urgence` tinyint(1) DEFAULT NULL,
  `motif` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `secretaire_id` (`secretaire_id`),
  CONSTRAINT `rendezvous_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`ident`),
  CONSTRAINT `rendezvous_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`ident`),
  CONSTRAINT `rendezvous_ibfk_3` FOREIGN KEY (`secretaire_id`) REFERENCES `secretaire_medicale` (`ident`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rendezvous`
--

LOCK TABLES `rendezvous` WRITE;
/*!40000 ALTER TABLE `rendezvous` DISABLE KEYS */;
INSERT INTO `rendezvous` VALUES (1,1,1,NULL,'2025-08-15','15:00:00','19:20:00','annulé',0,'plo,j','2025-08-18 01:39:54'),(2,1,1,1,'2025-08-15','15:00:00','19:20:00','confirmé',0,'plo,j','2025-08-18 01:50:04'),(3,1,1,NULL,'2025-08-23','08:00:00','12:00:00','confirmé',0,'pals','2025-08-18 09:59:30'),(4,1,1,NULL,'2025-08-12','10:02:00','05:03:00','terminé',0,'plo','2025-08-18 22:54:57'),(5,1,1,NULL,'2025-08-30','15:02:00','03:02:00','confirmé',0,'mlo','2025-08-18 22:55:23'),(6,1,1,NULL,'2025-08-22','12:00:00','13:54:00','confirmé',0,'poiuytreza','2025-08-18 23:55:35'),(7,3,1,NULL,'2025-08-23','23:05:00','05:05:00','confirmé',0,'kjhgvcx','2025-08-19 00:25:34'),(8,3,1,1,'2025-08-23','23:05:00','05:05:00','annulé',0,'kjhgvcx','2025-08-19 00:27:35'),(9,1,1,NULL,'2025-08-15','15:03:00','07:08:00','terminé',0,'sassss','2025-08-19 01:11:39'),(10,1,1,NULL,'2025-08-31','04:04:00','04:04:00','confirmé',0,'^ppppppp','2025-08-19 01:12:20'),(11,7,1,NULL,'2025-08-31','06:26:00','11:52:00','en attente',0,'856m','2025-08-20 00:47:18'),(12,7,1,1,'2025-08-20','22:05:00','13:52:00','terminé',0,'yhr','2025-08-20 13:07:23'),(13,4,1,1,'2025-08-05','23:05:00','05:55:00','terminé',0,'kjhjjj','2025-08-20 13:46:18'),(14,1,1,NULL,'2025-08-31','12:03:00','23:02:00','confirmé',0,'visite','2025-08-20 22:29:18'),(15,3,1,1,'2025-08-23','12:00:00','13:00:00','confirmé',0,'test','2025-08-20 22:33:27'),(16,1,1,NULL,'2025-08-15','12:05:00','06:35:00','en attente',0,'par','2025-08-21 11:59:01'),(17,2,3,1,'2025-08-24','15:00:00','17:00:00','annulé',0,'poihde','2025-08-21 23:17:21'),(18,2,NULL,NULL,'2025-08-31','12:00:00','17:00:00','en attente',0,'plo','2025-08-21 23:18:41'),(19,2,1,1,'2025-08-16','15:00:00','18:00:00','confirmé',0,'puun','2025-08-21 23:19:39'),(20,3,1,NULL,'2025-08-30','03:01:00','05:00:00','confirmé',0,'pkok','2025-08-21 23:24:38');
/*!40000 ALTER TABLE `rendezvous` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `secretaire_medicale`
--

DROP TABLE IF EXISTS `secretaire_medicale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `secretaire_medicale` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_secretaire` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_inscription` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nom_complet` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `sexe` enum('Homme','Femme') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `situation_matrimoniale` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `adresse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `pays` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ville` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code_postal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_telephone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_dimanche` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_lundi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mardi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_mercredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_jeudi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_vendredi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_debut_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heure_fin_samedi` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ident`),
  UNIQUE KEY `email_secretaire` (`email_secretaire`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `secretaire_medicale`
--

LOCK TABLES `secretaire_medicale` WRITE;
/*!40000 ALTER TABLE `secretaire_medicale` DISABLE KEYS */;
INSERT INTO `secretaire_medicale` VALUES (1,'eloge','secretaire@gmail.com','81dc9bdb52d04dc20036dbd8313ed055','2025-08-03 21:39:35','eloge GOMINA','2025-08-22','Femme',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'+228 91271004',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `secretaire_medicale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sortie`
--

DROP TABLE IF EXISTS `sortie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sortie` (
  `ident` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `sexe` varchar(10) NOT NULL,
  `date_naissance` date NOT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `numero_assurance` varchar(50) DEFAULT NULL,
  `motif` varchar(255) NOT NULL,
  `date_sortie` datetime NOT NULL,
  `observations` text,
  `admission_id` int DEFAULT NULL,
  PRIMARY KEY (`ident`),
  KEY `admission_id` (`admission_id`),
  CONSTRAINT `sortie_ibfk_1` FOREIGN KEY (`admission_id`) REFERENCES `admissions` (`ident`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sortie`
--

LOCK TABLES `sortie` WRITE;
/*!40000 ALTER TABLE `sortie` DISABLE KEYS */;
INSERT INTO `sortie` VALUES (1,'patient3','elodie','Femme','2025-08-14','lomer','123456','patient3@gmail.com','ojfoe','dfdfdfdf','2025-08-17 23:03:52','aaa',NULL),(2,'patient3','elodie','Femme','2025-08-14','lomer','123456','patient3@gmail.com','ojfoe','effef','2025-08-17 23:40:49','ffefef',7),(5,'eloge','patient','Homme','2025-08-03','telessous','+228 91271027','patient@gmail.com','','a','2025-08-18 00:10:38','',8),(6,'papou','1235','Femme','2025-08-15',' placeholder=','+228 91271004','papapap@gmail.com','','','2025-08-21 15:16:41','',9),(7,'patient','eloge','Homme','2065-08-03','telessous','+228 91271027','patient@gmail.com','','','2025-08-21 15:17:15','',12),(8,'patient','eloge','Homme','2065-08-03','telessous','+228 91271027','patient@gmail.com','','okijhyg','2025-08-21 23:01:05','jhjbn',13);
/*!40000 ALTER TABLE `sortie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-24  1:06:47
