-- Création de la base de données
CREATE DATABASE IF NOT EXISTS medijutsu;

-- Utilisation de la base de données
USE medijutsu;

-- Création de la table admin
CREATE TABLE admin (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email_admin VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Visualisation de la structure de la table
DESCRIBE admin;

-- Suppression de la table admin (si besoin de réinitialiser)
DROP TABLE admin;

-- Affichage des données de la table admin
SELECT * FROM admin;

-- creation de la table du docteur
CREATE TABLE doctor (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_doctor VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  groupe_sanguin VARCHAR(4) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Adresse et localisation
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Profil professionnel
  qualification TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  designation VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Visualisation de la structure de la table
DESCRIBE doctor;

-- Suppression de la table docteur
DROP TABLE doctor;

-- Affichage des données de la table admin
SELECT * FROM doctor;


-- creation de la table du patient
CREATE TABLE patient (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email_patient VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  etat_civil VARCHAR(50) DEFAULT NULL,
  profession VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  groupe_sanguin VARCHAR(4) DEFAULT NULL,
  tension_arterielle VARCHAR(20) DEFAULT NULL,
  taux_sucre VARCHAR(20) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Visualisation de la structure de la table
DESCRIBE patient;

-- Suppression de la table docteur
DROP TABLE patient;

-- Affichage des données de la table admin
SELECT * FROM patient;

-- Table secrétaire médicale
CREATE TABLE secretaire_medicale (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_secretaire VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Afficher la structure (description) de chaque table
DESCRIBE secretaire_medicale;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS secretaire_medicale;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM secretaire_medicale;

-- Table ambulancier
CREATE TABLE ambulancier (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_ambulancier VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- Afficher la structure (description) de chaque table
DESCRIBE ambulancier;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS ambulancier;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM ambulancier;



-- Table caissier
CREATE TABLE caissier (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_caissier VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- Afficher la structure (description) de chaque table
DESCRIBE caissier;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS caissier;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM caissier;


-- Table gestionnaire logistique
CREATE TABLE gestionnaire_logistique (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_logistique VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- Afficher la structure (description) de chaque table
DESCRIBE gestionnaire_logistique;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS gestionnaire_logistique;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM gestionnaire_logistique;



-- Table gestionnaire de stock
CREATE TABLE gestionnaire_stock (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_stock VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- Afficher la structure (description) de chaque table
DESCRIBE gestionnaire_stock;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS gestionnaire_stock;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM gestionnaire_stock;



-- Table infirmier
CREATE TABLE infirmier (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_infirmier VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- Afficher la structure (description) de chaque table
DESCRIBE infirmier;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS infirmier;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM infirmier;



-- Table interne en médecine
CREATE TABLE interne_medecine (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL UNIQUE,
  email_interne VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Informations personnelles
  nom_complet VARCHAR(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date_naissance DATE DEFAULT NULL,
  sexe ENUM('Homme', 'Femme') DEFAULT NULL,
  situation_matrimoniale VARCHAR(50) DEFAULT NULL,
  photo VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  -- Coordonnées
  adresse TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  pays VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  ville VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_postal VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  numero_telephone VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- Afficher la structure (description) de chaque table
DESCRIBE interne_medecine;
-- Supprimer chaque table si elle existe (utile avant une recréation)
DROP TABLE IF EXISTS interne_medecine;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM interne_medecine;

INSERT INTO test_consultation (
    date_consultation,date_confirmation,etat,patient_id,doctor_id,created_at,updated_at)
    VALUES (
    '2025-08-06',
    '2025-08-07',
    'confirmée',
    1,
    2,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

CREATE TABLE test_consultation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_consultation DATE,
    date_confirmation DATE,
    etat VARCHAR(50),
    patient_id INT,
    doctor_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);