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
-- DROP TABLE admin;

-- Affichage des données de la table admin
SELECT * FROM admin;




-- creation de la table du docteur
CREATE TABLE doctor (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
ALTER TABLE doctor
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;

-- Visualisation de la structure de la table
DESCRIBE doctor;

-- Suppression de la table docteur
-- DROP TABLE doctor;

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
ALTER TABLE patient
	ADD COLUMN actif BOOLEAN NOT NULL DEFAULT TRUE,
	ADD COLUMN derniere_connexion TIMESTAMP NULL DEFAULT NULL;
    
-- Visualisation de la structure de la table
DESCRIBE patient;

-- Suppression de la table docteur
-- DROP TABLE patient;

-- Affichage des données de la table admin
SELECT * FROM patient;

-- Table secrétaire médicale
	CREATE TABLE secretaire_medicale (
	  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
	  -- Identifiants et connexion
	  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
	ALTER TABLE secretaire_medicale
	  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
	  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
	  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
	  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
	  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
	  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
	  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
	  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
	  
	-- Afficher la structure (description) de chaque table
	DESCRIBE secretaire_medicale;
	-- Supprimer chaque table si elle existe (utile avant une recréation)
	-- DROP TABLE IF EXISTS secretaire_medicale;
	-- Sélectionner et afficher toutes les données présentes dans chaque table
	SELECT * FROM secretaire_medicale;


-- Table ambulancier
CREATE TABLE ambulancier (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
ALTER TABLE ambulancier
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
-- Afficher la structure (description) de chaque table
DESCRIBE ambulancier;
-- Supprimer chaque table si elle existe (utile avant une recréation)
-- DROP TABLE IF EXISTS ambulancier;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM ambulancier;



-- Table caissier
CREATE TABLE caissier (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
ALTER TABLE caissier
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
-- Afficher la structure (description) de chaque table
DESCRIBE caissier;
-- Supprimer chaque table si elle existe (utile avant une recréation)
-- DROP TABLE IF EXISTS caissier;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM caissier;


-- Table gestionnaire logistique
CREATE TABLE gestionnaire_logistique (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
ALTER TABLE gestionnaire_logistique
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
  -- Afficher la structure (description) de chaque table
DESCRIBE gestionnaire_logistique;
-- Supprimer chaque table si elle existe (utile avant une recréation)
-- DROP TABLE IF EXISTS gestionnaire_logistique;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM gestionnaire_logistique;



-- Table gestionnaire de stock
CREATE TABLE gestionnaire_stock (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
ALTER TABLE gestionnaire_stock
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
-- Afficher la structure (description) de chaque table
DESCRIBE gestionnaire_stock;
-- Supprimer chaque table si elle existe (utile avant une recréation)
-- DROP TABLE IF EXISTS gestionnaire_stock;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM gestionnaire_stock;



-- Table infirmier
CREATE TABLE infirmier (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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

ALTER TABLE infirmier
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
  -- Afficher la structure (description) de chaque table
DESCRIBE infirmier;
-- Supprimer chaque table si elle existe (utile avant une recréation)
-- DROP TABLE IF EXISTS infirmier;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM infirmier;



-- Table interne en médecine
CREATE TABLE interne_medecine (
  ident INT(11) AUTO_INCREMENT PRIMARY KEY, -- Clé primaire
  -- Identifiants et connexion
  nom_utilisateur VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
ALTER TABLE interne_medecine
  ADD heure_debut_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_dimanche VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_lundi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mardi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_mercredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_jeudi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_vendredi VARCHAR(10) DEFAULT NULL,
  ADD heure_debut_samedi VARCHAR(10) DEFAULT NULL,
  ADD heure_fin_samedi VARCHAR(10) DEFAULT NULL;
-- Afficher la structure (description) de chaque table
DESCRIBE interne_medecine;
-- Supprimer chaque table si elle existe (utile avant une recréation)
-- DROP TABLE IF EXISTS interne_medecine;
-- Sélectionner et afficher toutes les données présentes dans chaque table
SELECT * FROM interne_medecine;


-- table consultation

CREATE TABLE consultation (
        id INTEGER NOT NULL AUTO_INCREMENT,
        date_consultation DATE,
        motif VARCHAR(255),
        diagnostic TEXT,
        traitement TEXT,
        prescription TEXT,
        etat VARCHAR(20),
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(patient_id) REFERENCES patient (ident),
        FOREIGN KEY(doctor_id) REFERENCES doctor (ident)
);
ALTER TABLE consultation
ADD COLUMN date_confirmation DATETIME DEFAULT NULL;

-- Ajouter les colonnes
ALTER TABLE consultation
ADD COLUMN consultation_precedente_id INT NULL,
ADD COLUMN consultation_suivante_id INT NULL;

-- Ajouter les contraintes de clé étrangère (vers la même table)
ALTER TABLE consultation
ADD CONSTRAINT fk_consultation_precedente
  FOREIGN KEY (consultation_precedente_id)
  REFERENCES consultation(id)
  ON DELETE SET NULL
  ON UPDATE CASCADE;

ALTER TABLE consultation
ADD CONSTRAINT fk_consultation_suivante
  FOREIGN KEY (consultation_suivante_id)
  REFERENCES consultation(id)
  ON DELETE SET NULL
  ON UPDATE CASCADE;

SELECT * FROM consultation;

DROP TABLE consultation;


-- table consultation
CREATE TABLE admissions (
    ident INT AUTO_INCREMENT PRIMARY KEY,

    -- Informations personnelles du patient
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    sexe VARCHAR(10) NOT NULL,
    date_naissance DATE NOT NULL,
    adresse VARCHAR(255),
    telephone VARCHAR(20),
    email VARCHAR(120) NOT NULL,
    numero_assurance VARCHAR(50),

    -- Détails de l'admission
    motif VARCHAR(255) NOT NULL,
    date_admission DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Constantes vitales
    temperature FLOAT,
    tension VARCHAR(20),
    poids FLOAT,

    -- Observations
    observations TEXT,

    -- Personne à prévenir (fusionnée)
    pp_nom VARCHAR(100),
    pp_prenom VARCHAR(100),
    pp_telephone VARCHAR(20)
);
ALTER TABLE admissions 
CHANGE COLUMN sortie statut_sortie VARCHAR(100) DEFAULT 'non';

-- DROP TABLE admissions;

SELECT * FROM admissions;


CREATE TABLE sortie (
    ident INT AUTO_INCREMENT PRIMARY KEY,

    -- Informations personnelles du patient au moment de la sortie
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    sexe VARCHAR(10) NOT NULL,
    date_naissance DATE NOT NULL,
    adresse VARCHAR(255),
    telephone VARCHAR(20),
    email VARCHAR(120) NOT NULL,
    numero_assurance VARCHAR(50),

    -- Détails de l'admission
    motif VARCHAR(255) NOT NULL,

    -- Détails de la sortie
    date_sortie DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observations TEXT,

    -- Lien optionnel vers l’admission d’origine
    admission_id INT,
    CONSTRAINT fk_sortie_admission FOREIGN KEY (admission_id) REFERENCES admission(ident)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- DROP TABLE sortie;

SELECT * FROM sortie;


-- table rendezvous
CREATE TABLE rendezvous (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    patient_id INT NOT NULL,
    doctor_id INT DEFAULT NULL,
    secretaire_id INT DEFAULT NULL,
    
    date_rdv DATE NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    
    statut ENUM('en attente', 'confirmé', 'annulé', 'terminé') DEFAULT 'en attente',
    urgence BOOLEAN DEFAULT FALSE,
    motif TEXT DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Clés étrangères
    CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES patient(ident) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_doctor FOREIGN KEY (doctor_id) REFERENCES doctor(ident) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_secretaire FOREIGN KEY (secretaire_id) REFERENCES secretaire_medicale(ident) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- DROP TABLE rendezvous;
SELECT * FROM rendezvous;