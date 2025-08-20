from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#modele produit 
class Produit(db.Model):
    __tablename__='produits' 

    reference=db.Column(db.String(100),primary_key=True)
    nom_produit=db.Column(db.String(225))
    quantite=db.Column(db.Integer )
    

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

    actif = db.Column(db.Boolean, nullable=False, default=True)
    derniere_connexion = db.Column(db.DateTime, nullable=True)

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
    __tablename__ = 'consultation'  # correction : 2 underscores (et pas _tablename_)

    id = db.Column(db.Integer, primary_key=True)
    date_consultation = db.Column(db.DateTime, default=datetime.utcnow)
    date_confirmation = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin_consultation = db.Column(db.DateTime, nullable=True)

    # --- Liens entre consultations ---
    consultation_precedente_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=True)
    consultation_suivante_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=True)

    consultation_precedente = db.relationship(
        'Consultation', remote_side=[id], foreign_keys=[consultation_precedente_id], post_update=True,
        backref='consultation_suivante'
    )

    # --- Reste du modèle inchangé ---
    etat = db.Column(db.String(20), default='en_attente')

    motif = db.Column(db.String(255), nullable=True)
    plaintes = db.Column(db.Text, nullable=True)
    antecedents_personnels = db.Column(db.Text, nullable=True)
    antecedents_familiaux = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    traitements_en_cours = db.Column(db.Text, nullable=True)
    poids = db.Column(db.Float, nullable=True)
    taille = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    tension_arterielle = db.Column(db.String(10), nullable=True)
    frequence_cardiaque = db.Column(db.Integer, nullable=True)
    frequence_respiratoire = db.Column(db.Integer, nullable=True)
    saturation_oxygene = db.Column(db.Float, nullable=True)
    observations_cliniques = db.Column(db.Text, nullable=True)
    examens_biologiques = db.Column(db.Text, nullable=True)
    examens_radiologiques = db.Column(db.Text, nullable=True)
    autres_examens = db.Column(db.Text, nullable=True)
    resultats_examens = db.Column(db.Text, nullable=True)
    diagnostic = db.Column(db.Text, nullable=True)
    diagnostic_secondaire = db.Column(db.Text, nullable=True)
    traitement = db.Column(db.Text, nullable=True)
    traitement_non_medic = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.Text, nullable=True)
    conseils = db.Column(db.Text, nullable=True)
    prochain_rdv = db.Column(db.DateTime, nullable=True)
    note_suivi = db.Column(db.Text, nullable=True)
    ordonnance_jointe = db.Column(db.String(255), nullable=True)
    lettre_orientation = db.Column(db.String(255), nullable=True)
    documents_scannes = db.Column(db.String(255), nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.ident'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.ident'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


#modelle admision
class Admission(db.Model):
    __tablename__ = 'admissions'

    ident = db.Column(db.Integer, primary_key=True)

    # --- Informations personnelles du patient ---
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    numero_assurance = db.Column(db.String(50), nullable=True)

    # --- Détails de l'admission ---
    motif = db.Column(db.String(255), nullable=False)
    date_admission = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Constantes vitales ---
    temperature = db.Column(db.Float, nullable=True)
    tension = db.Column(db.String(20), nullable=True)
    poids = db.Column(db.Float, nullable=True)

    # --- Observations médicales ---
    observations = db.Column(db.Text, nullable=True)

    # --- Personne à prévenir (fusionnée) ---
    pp_nom = db.Column(db.String(100), nullable=True)
    pp_prenom = db.Column(db.String(100), nullable=True)
    pp_telephone = db.Column(db.String(20), nullable=True)

    # sortitr verification
    statut_sortie = db.Column(db.String(10), default="non", nullable=False)

    def __repr__(self):
        return f"<Admission {self.nom} {self.prenom} - {self.email}>"

class Sortie(db.Model):
    __tablename__ = 'sortie'

    ident = db.Column(db.Integer, primary_key=True)

    # --- Informations personnelles du patient au moment de la sortie ---
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    numero_assurance = db.Column(db.String(50), nullable=True)

    # --- Détails de l'admission ---
    motif = db.Column(db.String(255), nullable=False)

    # --- Détails de la sortie ---
    date_sortie = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    observations = db.Column(db.Text, nullable=True)  # Observations supplémentaires

    # --- Lien avec l'admission ---
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.ident'), nullable=True)
    admission = db.relationship('Admission', backref=db.backref('sortie', uselist=False))

#modelle secretaire medicale
class SecretaireMedicale(db.Model):
    __tablename__ = "secretaire_medicale"

    ident = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Identifiants et connexion
    nom_utilisateur = db.Column(db.String(100), default=None)
    email_secretaire = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_inscription = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    # Informations personnelles
    nom_complet = db.Column(db.String(225), default=None)
    date_naissance = db.Column(db.Date, default=None)
    sexe = db.Column(db.Enum('Homme', 'Femme'), default=None)
    situation_matrimoniale = db.Column(db.String(50), default=None)
    photo = db.Column(db.String(255), default=None)
    description = db.Column(db.Text, default=None)

    # Coordonnées
    adresse = db.Column(db.Text, default=None)
    pays = db.Column(db.String(30), default=None)
    ville = db.Column(db.String(30), default=None)
    code_postal = db.Column(db.String(20), default=None)
    numero_telephone = db.Column(db.String(15), default=None)

    # Horaires par jour
    heure_debut_dimanche = db.Column(db.String(10), default=None)
    heure_fin_dimanche = db.Column(db.String(10), default=None)
    heure_debut_lundi = db.Column(db.String(10), default=None)
    heure_fin_lundi = db.Column(db.String(10), default=None)
    heure_debut_mardi = db.Column(db.String(10), default=None)
    heure_fin_mardi = db.Column(db.String(10), default=None)
    heure_debut_mercredi = db.Column(db.String(10), default=None)
    heure_fin_mercredi = db.Column(db.String(10), default=None)
    heure_debut_jeudi = db.Column(db.String(10), default=None)
    heure_fin_jeudi = db.Column(db.String(10), default=None)
    heure_debut_vendredi = db.Column(db.String(10), default=None)
    heure_fin_vendredi = db.Column(db.String(10), default=None)
    heure_debut_samedi = db.Column(db.String(10), default=None)
    heure_fin_samedi = db.Column(db.String(10), default=None)

    def __repr__(self):
        return f"<SecretaireMedicale {self.nom_complet} ({self.email_secretaire})>"

# modele rendezvous
class RendezVous(db.Model):
    __tablename__ = 'rendezvous'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.ident'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.ident'), nullable=True)  # Nullable si secrétaire attribue
    secretaire_id = db.Column(db.Integer, db.ForeignKey('secretaire_medicale.ident'),
                              nullable=True)  # pour suivi attribution

    date_rdv = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, default=None, nullable=True)

    statut = db.Column(db.Enum('en attente', 'confirmé', 'annulé', 'terminé'), default='en attente')
    urgence = db.Column(db.Boolean, default=False)
    motif = db.Column(db.Text, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='rendezvous')
    doctor = db.relationship('Doctor', backref='rendezvous')
    secretaire = db.relationship('SecretaireMedicale', backref='rendezvous')
