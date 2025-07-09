from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# modele Pateint

class Patient(db.Model):
    __tablename__ = 'patient'

    ident = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(100))
    email_patient = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    nom_complet = db.Column(db.String(225))
    date_naissance = db.Column(db.Date)
    sexe = db.Column(db.Enum('Homme', 'Femme'))
    etat_civil = db.Column(db.String(50))
    profession = db.Column(db.String(100))
    groupe_sanguin = db.Column(db.String(4))
    tension_arterielle = db.Column(db.String(20))
    taux_sucre = db.Column(db.String(20))
    photo = db.Column(db.String(255))

    adresse = db.Column(db.Text)
    ville = db.Column(db.String(30))
    pays = db.Column(db.String(30))
    code_postal = db.Column(db.String(20))
    numero_telephone = db.Column(db.String(15))

    consultations = db.relationship('Consultation', backref='patient', lazy=True)


# modele docteur
class Doctor(db.Model):
    __tablename__ = 'doctor'

    ident = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(100))
    email_doctor = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    nom_complet = db.Column(db.String(225))
    date_naissance = db.Column(db.Date)
    sexe = db.Column(db.Enum('Homme', 'Femme'))
    situation_matrimoniale = db.Column(db.String(50))
    groupe_sanguin = db.Column(db.String(4))
    photo = db.Column(db.String(255))
    description = db.Column(db.Text)

    adresse = db.Column(db.Text)
    pays = db.Column(db.String(30))
    ville = db.Column(db.String(30))
    code_postal = db.Column(db.String(20))
    numero_telephone = db.Column(db.String(15))

    qualification = db.Column(db.Text)
    designation = db.Column(db.String(255))

    # Disponibilités hebdomadaires
    heure_debut_dimanche = db.Column(db.String(10))
    heure_fin_dimanche = db.Column(db.String(10))
    heure_debut_lundi = db.Column(db.String(10))
    heure_fin_lundi = db.Column(db.String(10))
    heure_debut_mardi = db.Column(db.String(10))
    heure_fin_mardi = db.Column(db.String(10))
    heure_debut_mercredi = db.Column(db.String(10))
    heure_fin_mercredi = db.Column(db.String(10))
    heure_debut_jeudi = db.Column(db.String(10))
    heure_fin_jeudi = db.Column(db.String(10))
    heure_debut_vendredi = db.Column(db.String(10))
    heure_fin_vendredi = db.Column(db.String(10))
    heure_debut_samedi = db.Column(db.String(10))
    heure_fin_samedi = db.Column(db.String(10))

    consultations = db.relationship('Consultation', backref='doctor', lazy=True)

# Modele Consultation
class Consultation(db.Model):
    __tablename__ = 'consultation'

    id = db.Column(db.Integer, primary_key=True)
    date_consultation = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin_consultation = db.Column(db.DateTime, nullable=True)

    motif = db.Column(db.String(255), nullable=True)
    diagnostic = db.Column(db.Text, nullable=True)
    traitement = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.Text, nullable=True)
    etat = db.Column(db.String(20), default='en_attente')  # en_attente, en_cours, terminee

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.ident'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.ident'), nullable=False)