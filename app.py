from flask import Flask, render_template, redirect, url_for, session, request, flash,make_response, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
from credentials import *
from flask_mail import Mail, Message
import re
from models import db, Consultation, Patient, Doctor, Admission, Sortie, Produit, SecretaireMedicale, RendezVous
from datetime import  datetime, date, time, timedelta
from flask_migrate import Migrate
from xhtml2pdf import pisa
from io import BytesIO
from functools import wraps



app = Flask(__name__)

# pour la base de donner
app.config['SECRET_KEY']=my_token
app.config['MYSQL_HOST'] = my_host
app.config['MYSQL_USER'] = my_user
app.config['MYSQL_PASSWORD'] = my_password
app.config['MYSQL_DB'] =  my_db
app.config['MYSQL_CURSORCLASS'] =my_CURSORCLASS

# pour la base de donner ORM
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{my_user}:{my_password}@{my_host}/{my_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


# Initialisation pour la mise a jour des tables lors de la modification du model
migrate = Migrate(app, db)

# initialisation de l'orm
db.init_app(app)

# Créer une table mm si elle n'existe pas
with app.app_context():
    db.create_all()

#pour l'envoie de Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = my_email
app.config['MAIL_PASSWORD'] = my_password_generer
app.config['MAIL_DEFAULT_SENDER'] = ('MediJutsu', 'elogegomina@gmail.com')

mail = Mail(app)

mysql = MySQL()
mysql.init_app(app)

app.secret_key = my_secret_key

#les pattern
pattern_email = r'(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))'
pattern_phone = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

"""debut decorateur autentification"""
# autentificaton
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_role = session.get('role')
            email_keys = {
                'admin': 'email_admin',
                'doctor': 'email_doctor',
                'patient': 'email_patient',
                'secretaire': 'email_secretaire',
                'ambulance': 'email_ambulancier',
                'caissier': 'email_caissier',
                'logistique': 'email_logistique',
                'stock': 'email_stock',
                'infirmier': 'email_infirmier',
                'interne': 'email_interne',
            }

            if not user_role or not session.get(email_keys.get(user_role)):
                flash("Vous devez être connecté", "warning")
                return redirect(url_for('login'))

            if role:
                # Gère liste ou string
                if isinstance(role, (list, tuple)):
                    if user_role not in role:
                        flash("Accès refusé", "danger")
                        return redirect(url_for('index'))
                else:
                    if user_role != role:
                        flash("Accès refusé", "danger")
                        return redirect(url_for('index'))

            return f(*args, **kwargs)
        return wrapped
    return decorator


"""fin decorateur authentifiation"""

"""debut admin"""
#admin
@app.route("/admin")
@login_required(role='admin')
def index():
    return render_template("admin/index_admin.html")

#admin liste admin
@app.route('/admin/liste_admin')
@login_required(role='admin')
def liste_admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT ident, nom_complet, email_admin, numero_telephone FROM admin")
    admins = cursor.fetchall()
    cursor.close()
    return render_template("admin/gestion_admin/liste_admin.html", admins=admins)

#suprimer admin
@app.route('/admin/supprimer/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def supprimer_admin(id):
    cursor = mysql.connection.cursor()
    try:
        # Supprimer l’admin avec l’identifiant donné
        cursor.execute("DELETE FROM admin WHERE ident = %s", (id,))
        mysql.connection.commit()
        flash("Administrateur supprimé avec succès.", "success")
    except Exception as e:
        flash("Erreur lors de la suppression : " + str(e), "danger")
    finally:
        cursor.close()

    # Redirection vers la liste des admins (ou une autre page)
    return redirect(url_for('liste_admin'))


#modifier admin
@app.route("/modifier-admin/<int:id>", methods=["GET", "POST"])
def modifier_admin(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        nom_complet = request.form['nom_complet']
        email = request.form['email_admin']
        numero_telephone = request.form['numero_telephone']

        # Exécution de la requête UPDATE
        cursor.execute("""
            UPDATE admin SET nom_complet=%s, email_admin=%s, numero_telephone=%s 
            WHERE ident=%s
        """, (nom_complet, email, numero_telephone, id))

        mysql.connection.commit()
        flash("Les informations ont été modifiées avec succès.", "success")
        return redirect(url_for('liste_admin'))  # attention au nom exact de la fonction liste

    # Sinon (GET), on affiche les infos actuelles dans le formulaire
    cursor.execute("SELECT * FROM admin WHERE ident = %s", (id,))
    admin = cursor.fetchone()
    return render_template("admin/gestion_admin/modifier_admin.html", admin=admin)


#liste docteur admin
@app.route("/admin/liste_docteur")
def liste_docteur_admin():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    return render_template("admin/gestion_docteur/Liste_docteur.html", doctors=doctors)

# uprimer admin
@app.route('/admin/supprimer_docteur/<int:id>')
@login_required(role='admin')
def supprimer_docteur(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM doctor WHERE ident = %s", (id,))
    mysql.connection.commit()
    flash("Médecin supprimé avec succès.", "success")
    return redirect(url_for('liste_docteur_admin'))

#profile admin
@app.route('/admin/voir/<int:id>')
@login_required(role='admin')
def voir_admin(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT ident, nom_complet, email_admin, numero_telephone, date_inscription FROM admin WHERE ident = %s", (id,))
    admin = cursor.fetchone()  # Un seul admin

    if not admin:
        flash("Administrateur introuvable.", "warning")
        return redirect(url_for('liste_admin'))

    return render_template("admin/gestion_admin/profile_admin.html", admin=admin)

# voir profile docteur par admin
@app.route('/admin/docteur/profile/<int:id>')
@login_required(role='admin')
def profile_doctor_admin(id):
    return render_template("admin/gestion_docteur/voir_profile_doctor.html")

# mmodifier profile docteur par admin
@app.route('/admin/docteur/modifier_profil/<int:id>')
@login_required(role='admin')
def modifier_profile_doctor_admin(id):

    return render_template("admin/gestion_docteur/modifier_docteur.html")

#liste des patient admin
@app.route("/admin/liste_patient")
@login_required(role='admin')
def liste_patient_admin():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()

    return render_template("admin/gestion_patient/liste_patient.html", patients=patients)

#modifier profiel pateint admin
@app.route('/admin/patient/<int:id>/modifier_profile')
@login_required(role='admin')
def modifier_profile_patient_admin(id):
    return render_template("admin/gestion_patient/modifier_patient.html")

#voir profile pateitn admin
@app.route('/admin/patient/<int:id>/voir_profile')
@login_required(role='admin')
def profile_patient_admin(id):
    return render_template("admin/gestion_patient/voir_profile_patient.html")

#surpimer pateirna admin
@app.route("/admin/patient/supprimer/<int:id>")
@login_required(role='admin')
def supprimer_patient_admin(id):
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM patient WHERE ident = %s", (id,))
    mysql.connection.commit()
    flash("Le patient a été supprimé avec succès.", "success")
    return redirect(url_for('liste_patient_admin'))

#liste secretaire medical admin
@app.route("/admin/liste_secretaire")
@login_required(role='admin')
def liste_secretaire_admin():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM secretaire_medicale")
    secretaires = cursor.fetchall()

    return render_template("admin/gestion_secretaire_medicale/liste_secretaire_medicale.html", secretaires=secretaires)

# supression secretaire medical admin
@app.route("/admin/secretaire/supprimer/<int:id>")
@login_required(role='admin')
def supprimer_secretaire_admin(id):
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM secretaire_medicale WHERE ident = %s", (id,))
    mysql.connection.commit()
    flash("Secrétaire médicale supprimée avec succès.", "success")
    return redirect(url_for('liste_secretaire_admin'))

#voir profile secretaire medical admin
@app.route("/admin/secretaire/<int:id>/profile")
@login_required(role='admin')
def voir_secretaire_admin(id):
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM secretaire_medicale WHERE ident = %s", (id,))
    secretaire = cursor.fetchone()

    if not secretaire:
        flash("Secrétaire introuvable.", "danger")
        return redirect(url_for('liste_secretaire_admin'))

    return render_template("admin/gestion_secretaire_medicale/voir_profile_secretaire_medicale.html", secretaire=secretaire)

# modifier profil secretaire medical admin
@app.route("/admin/secretaire/<int:id>/modifier", methods=['GET', 'POST'])
@login_required(role='admin')
def modifier_secretaire_admin(id):
    return render_template("admin/gestion_secretaire_medicale/modifier_secretaire_medicale.html")

"""fin admin"""



"""debut ambulance """
@app.route("/ambulance")
@login_required(role='ambulance')
def index_ambulance():
    return render_template("ambulance/index_ambulance.html")

@app.route("/modifier_profile_ambulancier")
@login_required(role='ambulance')
def modifier_profile_ambulancier():
    return render_template("ambulance/gestion_ambulance/modiifer_profile.html")
"""fin ambulance"""




"""debut caissier"""
@app.route("/caissier")
@login_required(role='caissier')
def index_caissier():
    return (render_template("caissier/index_caissier.html"))

@app.route("/caissier/modifier_profile_caissier")
@login_required(role='caissier')
def modifier_profile_caissier():
    return render_template("caissier/gestion_caissier/modiifer_profile.html")

"""fin caissier"""






"""debut docteur"""
# docteur
@app.route("/doctor")
@login_required(role='doctor')
def index_doctor():
    email_doctor = session.get('email_doctor')
    doctor = Doctor.query.filter_by(email_doctor=email_doctor).first()
    if not doctor:
        flash("Docteur non trouvé", "danger")
        return redirect(url_for('login'))

    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())

    # Nombre de rendez-vous aujourd'hui (consultations en attente ou en cours)
    rdv_count = Consultation.query.filter(
        Consultation.doctor_id == doctor.ident,
        Consultation.date_consultation >= today_start,
        Consultation.date_consultation <= today_end
    ).count()

    # Liste unique des patients du docteur (via ses consultations)
    patient_ids = db.session.query(Consultation.patient_id).filter(
        Consultation.doctor_id == doctor.ident
    ).distinct().all()
    patient_ids = [p[0] for p in patient_ids]

    patients = Patient.query.filter(Patient.ident.in_(patient_ids)).all()

    # Exemple de stats (à remplacer par tes vrais calculs)
    stats = [
        {"icon": "ri-empathize-line", "value": len(patients), "label": "Patients", "color": "primary",
         "change": "40% Plus élevé"},
        {"icon": "ri-lungs-line", "value": 20, "label": "Chirurgies", "color": "danger", "change": "26% Plus élevé"},
        {"icon": "ri-money-dollar-circle-line", "value": "$15K", "label": "Revenus", "color": "success",
         "change": "30% Plus élevé"},
    ]
    return render_template("doctor/index_doctor.html",
                           doctor=doctor,
                           rdv_count=rdv_count,
                           patients=patients,
                           stats=stats)

# liste docteur docteur
@app.route("/doctor/liste_doctor")
@login_required(role='doctor')
def liste_doctor():
    return render_template("doctor/gestion_docteur/liste_doctor.html")

# modification profile docteur
@app.route("/doctor/modifier_profile", methods=['GET', 'POST'])
@login_required(role='doctor')
def modifier_profile_doctor():
    if 'email_doctor' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))

    email = session['email_doctor']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        donnes = request.form
        nom_utilisateur = donnes.get('username')
        nom = donnes.get('nom')
        prenom = donnes.get('prenom')
        nom_complet = (nom + ' ' + prenom) if nom and prenom else None
        date_naissance = donnes.get('date_naissance')
        sexe = donnes.get('sexe')
        situation_matrimoniale = donnes.get('situation_matrimoniale')
        groupe_sanguin = donnes.get('groupe_sanguin')
        photo = donnes.get('photo')
        description = donnes.get('biography')
        adresse = donnes.get('adresse')
        pays = donnes.get('pays')
        ville = donnes.get('ville')
        code_postal = donnes.get('code_postal')
        numero_telephone = donnes.get('telephone')
        qualification = donnes.get('qualification')
        designation = donnes.get('designation')
        password = donnes.get('new_password')
        confirm_password = donnes.get('confirm_new_password')
        heure_debut_dimanche = donnes.get('dimanche_debut')
        heure_fin_dimanche = donnes.get('dimanche_fin')
        heure_debut_lundi = donnes.get('lundi_debut')
        heure_fin_lundi = donnes.get('lundi_fin')
        heure_debut_mardi = donnes.get('mardi_debut')
        heure_fin_mardi = donnes.get('mardi_fin')
        heure_debut_mercredi = donnes.get('mercredi_debut')
        heure_fin_mercredi = donnes.get('mercredi_fin')
        heure_debut_jeudi = donnes.get('jeudi_debut')
        heure_fin_jeudi = donnes.get('jeudi_fin')
        heure_debut_vendredi = donnes.get('vendredi_debut')
        heure_fin_vendredi = donnes.get('vendredi_fin')
        heure_debut_samedi = donnes.get('samedi_debut')
        heure_fin_samedi = donnes.get('samedi_fin')

        print(heure_fin_samedi)
        # Récupérer les anciennes données
        cursor.execute("SELECT * FROM doctor WHERE email_doctor = %s", (email,))
        ancien_profil = cursor.fetchone()

        if not ancien_profil:
            flash("Profil non trouvé.", "danger")
            return redirect(url_for('index_doctor'))

        # Vérification du nom d'utilisateur déjà utilisé par un autre compte
        if nom_utilisateur and nom_utilisateur != ancien_profil['nom_utilisateur']:
            cursor.execute("SELECT * FROM doctor WHERE nom_utilisateur = %s AND email_doctor != %s",
                           (nom_utilisateur, email))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Ce nom d'utilisateur est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

        # Gestion mot de passe
        if password:
            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas. Veuillez réessayer.", "danger")
                return redirect(request.url)
            hashed_password = hashlib.md5(password.encode()).hexdigest()
        else:
            hashed_password = ancien_profil['password']



        # Préparer les valeurs, en gardant l'ancienne si champ vide
        nom_utilisateur = nom_utilisateur or ancien_profil['nom_utilisateur']
        nom_complet = nom_complet or ancien_profil['nom_complet']
        date_naissance = date_naissance or ancien_profil['date_naissance']
        sexe = sexe or ancien_profil['sexe']
        situation_matrimoniale = situation_matrimoniale or ancien_profil['situation_matrimoniale']
        groupe_sanguin = groupe_sanguin or ancien_profil['groupe_sanguin']
        photo = photo or ancien_profil['photo']
        description = description or ancien_profil['description']
        adresse = adresse or ancien_profil['adresse']
        pays = pays or ancien_profil['pays']
        ville = ville or ancien_profil['ville']
        code_postal = code_postal or ancien_profil['code_postal']
        numero_telephone = numero_telephone or ancien_profil['numero_telephone']
        qualification = qualification or ancien_profil['qualification']
        designation = designation or ancien_profil['designation']
        heure_debut_dimanche = heure_debut_dimanche or ancien_profil.get('heure_debut_dimanche')
        heure_fin_dimanche = heure_fin_dimanche or ancien_profil.get('heure_fin_dimanche')
        heure_debut_lundi = heure_debut_lundi or ancien_profil.get('heure_debut_lundi')
        heure_fin_lundi = heure_fin_lundi or ancien_profil.get('heure_fin_lundi')
        heure_debut_mardi = heure_debut_mardi or ancien_profil.get('heure_debut_mardi')
        heure_fin_mardi = heure_fin_mardi or ancien_profil.get('heure_fin_mardi')
        heure_debut_mercredi = heure_debut_mercredi or ancien_profil.get('heure_debut_mercredi')
        heure_fin_mercredi = heure_fin_mercredi or ancien_profil.get('heure_fin_mercredi')
        heure_debut_jeudi = heure_debut_jeudi or ancien_profil.get('heure_debut_jeudi')
        heure_fin_jeudi = heure_fin_jeudi or ancien_profil.get('heure_fin_jeudi')
        heure_debut_vendredi = heure_debut_vendredi or ancien_profil.get('heure_debut_vendredi')
        heure_fin_vendredi = heure_fin_vendredi or ancien_profil.get('heure_fin_vendredi')
        heure_debut_samedi = heure_debut_samedi or ancien_profil.get('heure_debut_samedi')
        heure_fin_samedi = heure_fin_samedi or ancien_profil.get('heure_fin_samedi')

        # verifier si le numero est valide
        if numero_telephone==ancien_profil['numero_telephone']:
            pass
        elif re.match(pattern_phone, numero_telephone) :
            pass
        else:
            print("tel incorect")
            flash("phone number invalide", "danger")
            return redirect(request.url)
        try:
            cursor.execute("""
                            UPDATE doctor SET
                                nom_utilisateur=%s,
                                nom_complet=%s,
                                date_naissance=%s,
                                sexe=%s,
                                situation_matrimoniale=%s,
                                groupe_sanguin=%s,
                                photo=%s,
                                description=%s,
                                adresse=%s,
                                pays=%s,
                                ville=%s,
                                code_postal=%s,
                                numero_telephone=%s,
                                qualification=%s,
                                designation=%s,
                                password=%s,
                                heure_debut_dimanche=%s,
                                heure_fin_dimanche=%s,
                                heure_debut_lundi=%s,
                                heure_fin_lundi=%s,
                                heure_debut_mardi=%s,
                                heure_fin_mardi=%s,
                                heure_debut_mercredi=%s,
                                heure_fin_mercredi=%s,
                                heure_debut_jeudi=%s,
                                heure_fin_jeudi=%s,
                                heure_debut_vendredi=%s,
                                heure_fin_vendredi=%s,
                                heure_debut_samedi=%s,
                                heure_fin_samedi=%s
                            WHERE email_doctor=%s
                        """, (
                nom_utilisateur, nom_complet, date_naissance, sexe,
                situation_matrimoniale, groupe_sanguin, photo, description,
                adresse, pays, ville, code_postal, numero_telephone,
                qualification, designation, hashed_password,
                heure_debut_dimanche, heure_fin_dimanche,
                heure_debut_lundi, heure_fin_lundi,
                heure_debut_mardi, heure_fin_mardi,
                heure_debut_mercredi, heure_fin_mercredi,
                heure_debut_jeudi, heure_fin_jeudi,
                heure_debut_vendredi, heure_fin_vendredi,
                heure_debut_samedi, heure_fin_samedi,
                email
            ))

            mysql.connection.commit()
            cursor.close()
            flash("Profil mis à jour avec succès.", "success")
            return redirect(url_for('index_doctor'))

        except Exception as e:
            print("Erreur lors de la modification du profil :", e)
            flash("Erreur lors de la modification du profil.", "danger")
            return redirect(request.url)

    # En GET : Pré-remplir les champs
    cursor.execute("SELECT * FROM doctor WHERE email_doctor = %s", (email,))
    doctor = cursor.fetchone()
    cursor.close()

    # pour tout les pays
    pays = [
        "Afghanistan", "Afrique du Sud", "Albanie", "Algérie", "Allemagne", "Andorre", "Angola", "Antigua-et-Barbuda",
        "Arabie Saoudite", "Argentine", "Arménie", "Australie", "Autriche", "Azerbaïdjan", "Bahamas", "Bahreïn",
        "Bangladesh", "Barbade", "Belgique", "Belize", "Bénin", "Bhoutan", "Biélorussie", "Birmanie", "Bolivie",
        "Bosnie-Herzégovine", "Botswana", "Brésil", "Brunei", "Bulgarie", "Burkina Faso", "Burundi", "Cambodge",
        "Cameroun", "Canada", "Cap-Vert", "République centrafricaine", "Chili", "Chine", "Chypre", "Colombie",
        "Comores",
        "Congo (Brazzaville)", "Congo (RDC)", "Corée du Nord", "Corée du Sud", "Costa Rica", "Côte d'Ivoire", "Croatie",
        "Cuba", "Danemark", "Djibouti", "Dominique", "Égypte", "Émirats arabes unis", "Équateur", "Érythrée", "Espagne",
        "Estonie", "Eswatini", "États-Unis", "Éthiopie", "Fidji", "Finlande", "France", "Gabon", "Gambie", "Géorgie",
        "Ghana", "Grèce", "Grenade", "Guatemala", "Guinée", "Guinée-Bissau", "Guinée équatoriale", "Guyana", "Haïti",
        "Honduras", "Hongrie", "Inde", "Indonésie", "Irak", "Iran", "Irlande", "Islande", "Israël", "Italie",
        "Jamaïque",
        "Japon", "Jordanie", "Kazakhstan", "Kenya", "Kirghizistan", "Kiribati", "Koweït", "Laos", "Lesotho", "Lettonie",
        "Liban", "Libéria", "Libye", "Liechtenstein", "Lituanie", "Luxembourg", "Macédoine du Nord", "Madagascar",
        "Malaisie", "Malawi", "Maldives", "Mali", "Malte", "Maroc", "Îles Marshall", "Maurice", "Mauritanie", "Mexique",
        "Micronésie", "Moldavie", "Monaco", "Mongolie", "Monténégro", "Mozambique", "Namibie", "Nauru", "Népal",
        "Nicaragua", "Niger", "Nigeria", "Norvège", "Nouvelle-Zélande", "Oman", "Ouganda", "Ouzbékistan", "Pakistan",
        "Palaos", "Palestine", "Panama", "Papouasie-Nouvelle-Guinée", "Paraguay", "Pays-Bas", "Pérou", "Philippines",
        "Pologne", "Portugal", "Qatar", "Roumanie", "Royaume-Uni", "Russie", "Rwanda", "Saint-Kitts-et-Nevis",
        "Sainte-Lucie", "Saint-Marin", "Saint-Vincent-et-les-Grenadines", "Salomon", "Salvador", "Samoa",
        "São Tomé-et-Príncipe",
        "Sénégal", "Serbie", "Seychelles", "Sierra Leone", "Singapour", "Slovaquie", "Slovénie", "Somalie", "Soudan",
        "Soudan du Sud", "Sri Lanka", "Suède", "Suisse", "Suriname", "Syrie", "Tadjikistan", "Tanzanie", "Tchad",
        "République tchèque", "Thaïlande", "Timor oriental", "Togo", "Tonga", "Trinité-et-Tobago", "Tunisie",
        "Turkménistan",
        "Turquie", "Tuvalu", "Ukraine", "Uruguay", "Vanuatu", "Vatican", "Venezuela", "Viêt Nam", "Yémen", "Zambie",
        "Zimbabwe"
    ]

    return render_template("doctor/gestion_docteur/modifier_profile.html", pays=pays, doctor=doctor)

@app.route("/doctor/profile_doctor")
@login_required(role='doctor')
def profile_doctor():
    return render_template("doctor/gestion_docteur/profile_doctor.html")

#doctor patient
@app.route("/doctor/liste_patient")
@login_required(role='doctor')
def liste_patient_doctor():
    return render_template("doctor/gestion_patient/liste_patient.html")

#doctor conge presence
@app.route("/doctor/conge_presence/congé")
@login_required(role='doctor')
def conge_doctor():
    return render_template("doctor/conge_presence/conge.html")

@app.route("/doctor/conge_presence/présence")
@login_required(role='doctor')
def presence_doctor():
    return render_template("doctor/conge_presence/presence.html")

# doctor galeri et evenement
@app.route("/doctor/actualiter")
@login_required(role='doctor')
def actualiter_doctor():
    return render_template("doctor/galerie_&_evenement/actualiter.html")

@app.route("/doctor/evenement")
@login_required(role='doctor')
def evenement_doctor():
    return render_template("doctor/galerie_&_evenement/evenement.html")

@app.route("/doctor/galerie")
@login_required(role='doctor')
def galerie_doctor():
    return render_template("doctor/galerie_&_evenement/galerie.html")

# doctor ia
@app.route("/doctor/ia/resumer_dossier_medical")
@login_required(role='doctor')
def resumer_dossier_doctor():
    return render_template("doctor/gestion_ia/resumer_dossier.html")

@app.route("/doctor/ia/sugection_de_traitement")
@login_required(role='doctor')
def sugetion_doctor():
    return render_template("doctor/gestion_ia/sugection_traitement.html")

@app.route("/doctor/ia/surleillance_patient")
@login_required(role='doctor')
def surveillance_dossier_doctor():
    return render_template("doctor/gestion_ia/survellanc_patient.html")

# doctor messagerie
@app.route("/doctor/messagerie")
@login_required(role='doctor')
def messageire_doctor():
    return render_template("doctor/gestion_messagerie/messagerie.html")

#doctor hospitalisation
@app.route("/doctor/hospitalisation")
@login_required(role='doctor')
def hospitalisation_doctor():
    return render_template("doctor/hospitalisation/hospitalisation.html")

#parametre dcoctor
@app.route("/doctor/parametre")
@login_required(role='doctor')
def parametre_doctor():
    return render_template("doctor/parametre/parametre.html")

# fiche de paie doctor
@app.route("/doctor/salaire/fiche_de_paie")
@login_required(role='doctor')
def fiche_de_paie_doctor():
    return render_template("doctor/salaire/fiche_de_paie.html")

# dossiermedical doctor
@app.route("/doctor/dossier_medical")
@login_required(role='doctor')
def dossier_medical_doctor():
    return render_template("doctor/dossier_medical/dossier_medical.html")
@app.route("/doctor/ajout_patient")
@login_required(role='doctor')
def add_patient_doctor():
    return render_template("doctor/gestion_patient/ajout_patient.html")

@app.route("/doctor/modifier_patient")
@login_required(role='doctor')
def modifier_patient_doctor():
    return render_template("doctor/gestion_patient/modifier_patient.html")

"""fin docteur"""



"""debut gestionaire de stock"""
#gestonaire de stoCK
@app.route("/gestionaire_stock")
@login_required(role='stock')
def index_gestionaire_stock():
    return render_template("gestionaire_stock/index_gestionaire_stock.html")

@app.route("/gestionaire_stock/modifier_profile_stock")
@login_required(role='stock')
def modifier_profile_stock():
    return render_template("gestionaire_stock/gestion_ambulance/modiifer_profile.html")


"""fin gestionnaire de stock"""

@app.route("/infirmier")
@login_required(role='patient')
def index_infirmier():
    return render_template("infirmier/index_infirmier.html")

@app.route("/infirmier/modifier_profile_infirmier")
@login_required(role='infirmier')
def modifier_profile_infirmier():
    return render_template("infirmier/gestion_infirmier/modiifer_profile.html")




"""debut patient"""
@app.route("/patient")
@login_required(role='patient')
def index_patient():
    # Récupération de l'email du patient stocké en session
    email_patient = session.get('email_patient')
    if not email_patient:
        flash("Vous devez être connecté", "warning")
        return redirect(url_for('login'))

    # Récupération du patient depuis la base
    patient = Patient.query.filter_by(email_patient=email_patient).first()
    if not patient:
        flash("Patient introuvable", "danger")
        return redirect(url_for('login'))

    # Exemple : récupérer tous les rapports liés à ce patient
    # Ici tu peux adapter selon ton modèle de rapports (Consultation, etc.)
    rapports = Consultation.query.filter_by(patient_id=patient.ident).all()
    if patient.date_naissance:
        today = date.today()
        patient.age = today.year - patient.date_naissance.year - (
                    (today.month, today.day) < (patient.date_naissance.month, patient.date_naissance.day))
    else:
        patient.age = "Non renseigné"
    return render_template(
        "patient/index_patient.html",
        patient=patient,
        rapports=[{"nom": r.motif or "Consultation", "date": r.date_consultation.strftime("%d/%m/%Y")} for r in rapports],
        rapport_detail=None  # tu peux remplacer par un rapport spécifique si nécessaire
    )





# modifier profile patient
@app.route('/patient/profile/modifier', methods=['GET', 'POST'])
@login_required(role='patient')
def modifier_profile_patient():
    if 'email_patient' not in session:
        flash("Veuillez vous connecter pour accéder à cette page.", "warning")
        return redirect(url_for('login'))

    email = session['email_patient']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # pour tout les pays
    pays = [
        "Afghanistan", "Afrique du Sud", "Albanie", "Algérie", "Allemagne", "Andorre", "Angola",
        "Antigua-et-Barbuda",
        "Arabie Saoudite", "Argentine", "Arménie", "Australie", "Autriche", "Azerbaïdjan", "Bahamas", "Bahreïn",
        "Bangladesh", "Barbade", "Belgique", "Belize", "Bénin", "Bhoutan", "Biélorussie", "Birmanie", "Bolivie",
        "Bosnie-Herzégovine", "Botswana", "Brésil", "Brunei", "Bulgarie", "Burkina Faso", "Burundi", "Cambodge",
        "Cameroun", "Canada", "Cap-Vert", "République centrafricaine", "Chili", "Chine", "Chypre", "Colombie",
        "Comores",
        "Congo (Brazzaville)", "Congo (RDC)", "Corée du Nord", "Corée du Sud", "Costa Rica", "Côte d'Ivoire",
        "Croatie",
        "Cuba", "Danemark", "Djibouti", "Dominique", "Égypte", "Émirats arabes unis", "Équateur", "Érythrée",
        "Espagne",
        "Estonie", "Eswatini", "États-Unis", "Éthiopie", "Fidji", "Finlande", "France", "Gabon", "Gambie",
        "Géorgie",
        "Ghana", "Grèce", "Grenade", "Guatemala", "Guinée", "Guinée-Bissau", "Guinée équatoriale", "Guyana",
        "Haïti",
        "Honduras", "Hongrie", "Inde", "Indonésie", "Irak", "Iran", "Irlande", "Islande", "Israël", "Italie",
        "Jamaïque",
        "Japon", "Jordanie", "Kazakhstan", "Kenya", "Kirghizistan", "Kiribati", "Koweït", "Laos", "Lesotho",
        "Lettonie",
        "Liban", "Libéria", "Libye", "Liechtenstein", "Lituanie", "Luxembourg", "Macédoine du Nord", "Madagascar",
        "Malaisie", "Malawi", "Maldives", "Mali", "Malte", "Maroc", "Îles Marshall", "Maurice", "Mauritanie",
        "Mexique",
        "Micronésie", "Moldavie", "Monaco", "Mongolie", "Monténégro", "Mozambique", "Namibie", "Nauru", "Népal",
        "Nicaragua", "Niger", "Nigeria", "Norvège", "Nouvelle-Zélande", "Oman", "Ouganda", "Ouzbékistan",
        "Pakistan",
        "Palaos", "Palestine", "Panama", "Papouasie-Nouvelle-Guinée", "Paraguay", "Pays-Bas", "Pérou",
        "Philippines",
        "Pologne", "Portugal", "Qatar", "Roumanie", "Royaume-Uni", "Russie", "Rwanda", "Saint-Kitts-et-Nevis",
        "Sainte-Lucie", "Saint-Marin", "Saint-Vincent-et-les-Grenadines", "Salomon", "Salvador", "Samoa",
        "São Tomé-et-Príncipe",
        "Sénégal", "Serbie", "Seychelles", "Sierra Leone", "Singapour", "Slovaquie", "Slovénie", "Somalie",
        "Soudan",
        "Soudan du Sud", "Sri Lanka", "Suède", "Suisse", "Suriname", "Syrie", "Tadjikistan", "Tanzanie", "Tchad",
        "République tchèque", "Thaïlande", "Timor oriental", "Togo", "Tonga", "Trinité-et-Tobago", "Tunisie",
        "Turkménistan",
        "Turquie", "Tuvalu", "Ukraine", "Uruguay", "Vanuatu", "Vatican", "Venezuela", "Viêt Nam", "Yémen", "Zambie",
        "Zimbabwe"
    ]
    # Récupération des données existantes
    cursor.execute("SELECT * FROM patient WHERE email_patient = %s", (email,))
    patient = cursor.fetchone()

    if not patient:
        flash("Profil non trouvé.", "danger")
        cursor.close()
        return redirect(url_for('index_patient'))

    if request.method == 'POST':
        data = request.form

        nom_utilisateur = data.get('nom_utilisateur') or patient['nom_utilisateur']
        nom = data.get('nom')
        prenom = data.get('prenom')
        nom_complet = (nom + ' ' + prenom) if nom and prenom else None
        date_naissance = data.get('date_naissance') or patient['date_naissance']
        sexe = data.get('sexe') or patient['sexe']
        etat_civil = data.get('etat_civil') or patient['etat_civil']
        profession = data.get('profession') or patient['profession']
        groupe_sanguin = data.get('groupe_sanguin') or patient['groupe_sanguin']
        tension_arterielle = data.get('tension_arterielle') or patient['tension_arterielle']
        taux_sucre = data.get('taux_sucre') or patient['taux_sucre']
        adresse = data.get('adresse') or patient['adresse']
        ville = data.get('ville') or patient['ville']
        pays = data.get('pays') or patient['pays']
        code_postal = data.get('code_postal') or patient['code_postal']
        numero_telephone = data.get('numero_telephone') or patient['numero_telephone']

        # Vérification du nom d'utilisateur déjà utilisé par un autre compte
        if nom_utilisateur and nom_utilisateur != patient['nom_utilisateur']:
            cursor.execute("SELECT * FROM patient WHERE nom_utilisateur = %s AND email_patient != %s",
                           (nom_utilisateur, email))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Ce nom d'utilisateur est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

        # Nouveau mot de passe
        password = data.get('new_password')
        confirm_password = data.get('confirm_new_password')

        if password:
            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas.", "danger")
                cursor.close()
                return redirect(request.url)
            password_hash = hashlib.md5(password.encode()).hexdigest()
        else:
            password_hash = patient['password']

        # Vérif téléphone (si changé)
        if numero_telephone != patient['numero_telephone']:
            if not re.match(pattern_phone, numero_telephone):
                flash("Numéro de téléphone invalide.", "danger")
                cursor.close()
                return redirect(request.url)

        try:
            cursor.execute("""
                UPDATE patient SET
                    nom_utilisateur=%s,
                    nom_complet=%s,
                    date_naissance=%s,
                    sexe=%s,
                    etat_civil=%s,
                    profession=%s,
                    groupe_sanguin=%s,
                    tension_arterielle=%s,
                    taux_sucre=%s,
                    adresse=%s,
                    ville=%s,
                    pays=%s,
                    code_postal=%s,
                    numero_telephone=%s,
                    password=%s
                WHERE email_patient=%s
            """, (
                nom_utilisateur, nom_complet, date_naissance, sexe,
                etat_civil, profession, groupe_sanguin, tension_arterielle,
                taux_sucre, adresse, ville, pays, code_postal,
                numero_telephone, password_hash, email
            ))

            mysql.connection.commit()
            cursor.close()
            flash("Profil mis à jour avec succès.", "success")
            return redirect(url_for('index_patient'))

        except Exception as e:
            print("Erreur :", e)
            flash("Erreur lors de la mise à jour du profil.", "danger")
            cursor.close()
            return redirect(request.url)


    return render_template("patient/gestion_patient/modifier_profile.html", patient=patient, pays=pays)

@app.route('/patient/profile')
@login_required(role='patient')
def profile_patient():
    return render_template('patient/gestion_patient/profile_patient.html')



"""fin patient"""



"""debut secretaire secretaire medical"""
#secretaiere medical
@app.route("/secretaire_medicales")
@login_required(role='secretaire')
def index_secretaire_medicales():
    # Nombre de rendez-vous aujourd'hui
    total_rdv_today = RendezVous.query.filter(RendezVous.date_rdv == date.today()).count()

    # Total admissions
    total_admissions = Admission.query.count()

    # Total sorties
    total_sorties = Sortie.query.count()

    # Liste des prochains rendez-vous (par exemple 10 prochains)
    rendezvous = (
        RendezVous.query
        .filter(RendezVous.date_rdv >= date.today(), RendezVous.statut == 'en attente')
        .order_by(RendezVous.date_rdv.asc())
        .limit(10)
        .all()
    )

    # Liste des admissions récentes (par exemple 10 dernières)
    admissions = Admission.query.order_by(Admission.date_admission.desc()).limit(10).all()

    # Liste des sorties récentes (par exemple 10 dernières)
    sorties = Sortie.query.order_by(Sortie.date_sortie.desc()).limit(10).all()

    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_last_week = start_of_week - timedelta(days=7)
    end_of_last_week = start_of_week - timedelta(seconds=1)

    # Comptage des patients inscrits cette semaine
    patients_this_week = Patient.query.filter(Patient.date_inscription >= start_of_week).count()

    # Comptage des patients inscrits la semaine dernière
    patients_last_week = Patient.query.filter(
        Patient.date_inscription >= start_of_last_week,
        Patient.date_inscription <= end_of_last_week
    ).count()

    # Calcul du pourcentage
    if patients_last_week > 0:
        pourcentage = ((patients_this_week - patients_last_week) / patients_last_week) * 100
    else:
        pourcentage = 100 if patients_this_week > 0 else 0

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    labels = []
    data = []

    for i in range(7):
        jour = start_of_week + timedelta(days=i)
        labels.append(jour.strftime("%A"))  # ex: Lundi, Mardi…
        count = RendezVous.query.filter(
            RendezVous.date_rdv == jour
        ).count()
        data.append(count)

    return render_template(
        "secretaire_medicales/index_secretaire_medicales.html",
        total_rdv_today=total_rdv_today,
        total_admissions=total_admissions,
        total_sorties=total_sorties,
        rendezvous=rendezvous,
        admissions=admissions,
        sorties=sorties,
        patients_this_week=patients_this_week,
        patients_last_week=patients_last_week,
        pourcentage=round(pourcentage),
                           labels=labels, data=data
    )

@app.route('/rendezvous/confirmer/<int:rdv_id>')
def confirmer_rendezvous(rdv_id):
    rdv = RendezVous.query.get(rdv_id)
    if rdv:
        rdv.statut = 'confirmé'  # ou ce que tu utilises comme champ statut
        db.session.commit()
    return redirect(url_for('index_secretaire_medicales'))


"""admission"""
#admission_patient  secretaire medicale
@app.route("/secretaire_medicales/admission_patient", methods=['GET', 'POST'])
@login_required(role='secretaire')
def admission_patient():
    patients = Patient.query.all()
    patients_data = []

    for p in patients:
        # admission_patient et liste des admissions – gérés par la secrétaire médicale
        if p.nom_complet:
            nom_parts = p.nom_complet.split(' ', 1)
            nom = nom_parts[0]
            prenom = nom_parts[1] if len(nom_parts) > 1 else ''
        else:
            nom = ''
            prenom = ''

        patients_data.append({
            'ident': p.ident,
            'nom': nom,
            'prenom': prenom,
            'telephone': p.numero_telephone,
            'email': p.email_patient,
            'date_naissance': p.date_naissance.strftime('%Y-%m-%d') if p.date_naissance else '',
            'sexe': p.sexe if p.sexe else '',
            'adresse': p.adresse if p.adresse else '',
        })

    if request.method == "POST":
        # Récupérer les données du formulaire
        patient_id = request.form.get("patient_id")
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        adresse = request.form.get("adresse")
        date_naissance = request.form.get("date_naissance")
        sexe = request.form.get("sexe")
        numero_assurance = request.form.get("numero_assurance")
        motif = request.form.get("motif")
        temperature = request.form.get("temperature")
        tension = request.form.get("tension")
        poids = request.form.get("poids")
        observations = request.form.get("observations")

        # Personne à prévenir
        pp_nom = request.form.get("pp_nom")
        pp_prenom = request.form.get("pp_prenom")
        pp_telephone = request.form.get("pp_telephone")

        # les verification
        existing_user = Patient.query.filter_by(email_patient=email).first()

        if not patient_id and existing_user:
            patient_id = existing_user.ident

        if re.match(pattern_email, email):
            pass
        else:
            flash("Votre email est invalide", "danger")
            return redirect(request.url)

        # Sécuriser les conversions
        try:
            date_naissance_dt = datetime.strptime(date_naissance, "%Y-%m-%d") if date_naissance else None
        except ValueError:
            flash("Date de naissance invalide.", "danger")
            return redirect(request.referrer)

        try:
            temperature = float(temperature) if temperature else None
        except ValueError:
            flash("Température invalide.", "danger")
            return redirect(request.referrer)

        try:
            poids = float(poids) if poids else None
        except ValueError:
            flash("Poids invalide.", "danger")
            return redirect(request.referrer)

        # --- Vérifier si patient existe ou créer ---
        if not patient_id:
            nom_complet = f"{nom} {prenom}".strip()
            existing_patient = Patient.query.filter_by(nom_complet=nom_complet, email_patient=email).first()

            if not existing_patient:
                # Mot de passe statique "1234" haché
                default_password = "1234"
                hashed_password = hashlib.md5(default_password.encode()).hexdigest()

                new_patient = Patient(
                    nom_complet=nom_complet,
                    email_patient=email,
                    password=hashed_password,
                    date_naissance=datetime.strptime(date_naissance, "%Y-%m-%d") if date_naissance else None,
                    numero_telephone=telephone,
                    adresse=adresse,
                    sexe=sexe,
                    actif=True
                )
                db.session.add(new_patient)
                db.session.flush()  # pour récupérer new_patient.ident sans commit
                patient_id = new_patient.ident
            else:
                patient_id = existing_patient.ident

        # --- Créer l'admission ---
        try:
            admission = Admission(
                nom=nom,
                prenom=prenom,
                sexe=sexe,
                date_naissance=date_naissance_dt,
                adresse=adresse,
                telephone=telephone,
                email=email,
                numero_assurance=numero_assurance,
                motif=motif,
                temperature=temperature,
                tension=tension,
                poids=poids,
                observations=observations,
                pp_nom=pp_nom,
                pp_prenom=pp_prenom,
                pp_telephone=pp_telephone
            )
            db.session.add(admission)
            db.session.commit()
            flash("Admission enregistrée avec succès", "success")
            return redirect(url_for("liste_admissions"))
        except Exception as e:
            db.session.rollback()
            print("eloge .................................", e)
            flash("Erreur lors de l'enregistrement de l'admission.", "danger")
            return redirect(request.referrer)

    return render_template("secretaire_medicales/gestion_patients/admissions_patient.html", patients=patients_data)

#sortie_patient  secretaire medicale
@app.route("/secretaire/sortie/<int:admission_id>", methods=['GET', 'POST'])
@login_required(role='secretaire')
def creer_sortie(admission_id):
    # Récupérer l'admission
    admission = Admission.query.get_or_404(admission_id)

    if request.method == 'POST':
        # Récupérer les champs du formulaire
        motif_sortie = request.form.get('motif')
        observations_supp = request.form.get('observations')

        # Créer la sortie
        sortie = Sortie(
            nom=admission.nom,
            prenom=admission.prenom,
            sexe=admission.sexe,
            date_naissance=admission.date_naissance,
            adresse=admission.adresse,
            telephone=admission.telephone,
            email=admission.email,
            numero_assurance=admission.numero_assurance,
            motif=motif_sortie or admission.motif,
            date_sortie=datetime.utcnow(),
            observations=observations_supp,
            admission=admission
        )

        db.session.add(sortie)

        # Mise à jour du statut de sortie dans Admission
        admission.statut_sortie = "oui"

        db.session.commit()

        # Stocker l'ID de l'admission dans la session si besoin
        session['last_admission_id'] = admission.ident

        flash('Sortie du patient enregistrée avec succès.', 'success')
        return redirect(url_for('liste_sorties'))

    # GET : afficher le formulaire
    return render_template(
        "secretaire_medicales/gestion_patients/sortie_patient.html",
        admission=admission
    )




#liste des admition et qui permet la sortie

@app.route("/secretaire_medicales/liste_admission")
@login_required(role='secretaire')
def liste_admissions():
    admissions = Admission.query.all()
    print(admissions)
    return render_template("secretaire_medicales/gestion_patients/liste_admissions.html", admissions=admissions)

#modifier admission
@app.route('/admission/modifier/<int:admission_id>', methods=['GET', 'POST'])
def modifier_admission(admission_id):
    admission = Admission.query.get_or_404(admission_id)

    if request.method == 'POST':
        # Récupère les données du formulaire modifié
        admission.nom = request.form.get('nom')
        admission.prenom = request.form.get('prenom')
        admission.sexe = request.form.get('sexe')

        date_naissance = request.form.get('date_naissance')
        if date_naissance:
            admission.date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d')

        admission.adresse = request.form.get('adresse')
        admission.telephone = request.form.get('telephone')
        admission.email = request.form.get('email')
        admission.numero_assurance = request.form.get('numero_assurance')
        admission.motif = request.form.get('motif')
        admission.temperature = float(request.form.get('temperature')) if request.form.get('temperature') else None
        admission.tension = request.form.get('tension')
        admission.poids = float(request.form.get('poids')) if request.form.get('poids') else None
        admission.observations = request.form.get('observations')

        admission.pp_nom = request.form.get('pp_nom')
        admission.pp_prenom = request.form.get('pp_prenom')
        admission.pp_telephone = request.form.get('pp_telephone')

        db.session.commit()
        flash("Admission modifiée avec succès.", "success")
        return redirect(url_for('liste_admission'))

    # En GET, on affiche le formulaire pré-rempli
    return render_template("secretaire_medicales/gestion_patients/admissions_patient.html", admission=admission)

#modifier sortie
@app.route("/secretaire_medicales/sorties/modifier/<int:sortie_id>", methods=["GET", "POST"])
@login_required(role="secretaire")
def modifier_sortie(sortie_id):
    sortie = Sortie.query.get_or_404(sortie_id)

    if request.method == "POST":
        sortie.observations = request.form.get("observations")
        db.session.commit()
        flash("Sortie modifiée avec succès.", "success")
        return redirect(url_for("liste_sorties"))

    return render_template("secretaire_medicales/gestion_patients/sortie_patient.html", sortie=sortie)
#suprimer admission
@app.route('/secretaire/admission/supprimer/<int:admission_id>', methods=['GET', 'POST'])
@login_required(role="secretaire")
def supprimer_admission(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    try:
        db.session.delete(admission)
        db.session.commit()
        flash("Admission supprimée avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "danger")
    return redirect(url_for('liste_admissions'))

#sprimer sortie
@app.route('/secretaire/sortie/supprimer/<int:sortie_id>', methods=['GET', 'POST'])
@login_required(role='secretaire')
def supprimer_sortie(sortie_id):
    sortie = Sortie.query.get_or_404(sortie_id)
    try:
        # Optionnel : remettre le statut_sortie de l'admission à "non"
        if sortie.admission:
            sortie.admission.statut_sortie = "non"

        db.session.delete(sortie)
        db.session.commit()
        flash("Sortie du patient supprimée avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "danger")
    return redirect(url_for('liste_sorties'))


# voir admission
@app.route('/admission/<int:admission_id>')
@login_required(role="secretaire")
def voir_admission(admission_id):
    admission = Admission.query.get(admission_id)
    if not admission:
        pass
    return render_template('secretaire_medicales/gestion_patients/voir_admission.html', admission=admission)

#coir admission patient
@app.route('/patient/detail/admission/<int:admission_id>')
@login_required(role='patient')
def voir_admission_patient(admission_id):
    admission = Admission.query.get_or_404(admission_id)

    # 🔹 Récupérer le patient lié
    patient = Patient.query.filter_by(email_patient=admission.email).first()

    return render_template(
        'patient/gestion_dossier_medical/voir_admission.html',
        admission=admission,
        patient=patient  # <-- maintenant disponible dans le template
    )


#voir admission docteur
@app.route('/doctor/detail/admission/<int:admission_id>')
@login_required(role='doctor')
def voir_admission_doctor(admission_id):
    admission = Admission.query.get_or_404(admission_id)

    # 🔹 Récupérer le patient lié
    patient = Patient.query.filter_by(email_patient=admission.email).first()

    return render_template(
        'doctor/dossier_medical/voir_admission.html',
        admission=admission,
        patient=patient  # <-- maintenant disponible dans le template
    )

#voir sortie secretaire
@app.route("/secretaire_medicales/sortie/<int:sortie_id>")
@login_required(role='secretaire')
def voir_sortie(sortie_id):
    sortie = Sortie.query.get_or_404(sortie_id)
    # Récupérer le patient via l'admission liée
    patient = None
    if sortie.admission:
        patient = Patient.query.filter_by(email_patient=sortie.admission.email).first()
    return render_template("secretaire_medicales/gestion_patients/voir_sortie_patient.html", sortie=sortie, patient=patient)

#voir sortie patient
@app.route("/patient/sortie/<int:sortie_id>")
@login_required(role='patient')
def voir_sortie_patient(sortie_id):
    sortie = Sortie.query.get_or_404(sortie_id)

    # 🔹 Récupérer le patient lié via l'admission
    patient = None
    if sortie.admission:
        patient = Patient.query.filter_by(email_patient=sortie.admission.email).first()

    return render_template(
        "patient/gestion_dossier_medical/voir_sortie_patient.html",
        sortie=sortie,
        patient=patient  # <-- maintenant disponible
    )

#voir soirtie docteur
@app.route("/docteur/sortie/<int:sortie_id>")
@login_required(role='doctor')
def voir_sortie_doctor(sortie_id):
    sortie = Sortie.query.get_or_404(sortie_id)

    # 🔹 Récupérer le patient lié via l'admission
    patient = None
    if sortie.admission:
        patient = Patient.query.filter_by(email_patient=sortie.admission.email).first()

    return render_template(
        "doctor/dossier_medical/voir_sortie_patient.html",
        sortie=sortie,
        patient=patient  # <-- maintenant disponible
    )


#liste sortie patient secretaire medicale
@app.route("/secretaire_medicales/liste_sortie_patient")
@login_required(role='secretaire')
def liste_sorties():
    sorties = Sortie.query.order_by(Sortie.date_sortie.desc()).all()
    return render_template('secretaire_medicales/gestion_patients/liste_sortie_patient.html', sorties=sorties)


# #inscription du patient secretaire
@app.route("/secretaire/gestion_patient/signup_patient_secretaire", methods=['GET', 'POST'])
@login_required(role='secretaire')
def signup_patient_secretaire():
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM patient WHERE email_patient = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            # verifier si email est valide
            if re.match(pattern_email, email):
                pass
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)
            try:
                cursor.execute("""INSERT INTO patient (email_patient, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le patient
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('liste_patient_secretaire'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('secretaire_medicales/gestion_patients/signup.html')

#liste des patient secretaire
@app.route("/secretaire/gestion_patient/liste_patient")
@login_required(role='secretaire')
def liste_patient_secretaire():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()

    return render_template("secretaire_medicales/gestion_patients/liste_patient.html", patients=patients)

#modification_patients secretaire medicale
@app.route("/secretaire_medicales/modification_patients")
@login_required(role='secretaire')
def modification_patients():
    return render_template("secretaire_medicales/gestion_patients/modification_patients.html")

#fiche_de_paie secretaire medicale
@app.route("/secretaire_medicales/fiche_de_paie")
@login_required(role='secretaire')
def fiche_de_paie():
    return render_template("secretaire_medicales/gestion_salaire/fiche_de_paie.html")

#messagerie secretaire medicale
@app.route("/secretaire_medicales/messagerie")
@login_required(role='secretaire')
def messagerie():
    return render_template("secretaire_medicales/gestion_messageries/messagerie.html")

#liste_departement secretaire medicale
@app.route("/secretaire_medicales/liste_departement")
@login_required(role='secretaire')
def liste_departement():
    return render_template("secretaire_medicales/gestion_departement/liste_departement.html")

#congé_personnel secretaire medicale
@app.route("/secretaire_medicales/congé_personnel")
@login_required(role='secretaire')
def congé_personnel():
    return render_template("secretaire_medicales/gestion_congé_presence/congé_personnel.html")

#présence_assiduité secretaire medicale
@app.route("/secretaire_medicales/presence_assiduite")
@login_required(role='secretaire')
def presence_assiduite():
    return render_template("secretaire_medicales/gestion_congé_presence/presence_assiduite.html")

#Reserver_chambre secretaire medicale
@app.route("/secretaire_medicales/Reserver_chambre")
@login_required(role='secretaire')
def Reserver_chambre():
    return render_template("secretaire_medicales/Gestion_chambre/Reserver_chambre.html")

#add_ambulance secretaire medicale
@app.route("/secretaire_medicales/add_ambulance")
@login_required(role='secretaire')
def add_ambulance():
    return render_template("secretaire_medicales/gestion_ambulance/add_ambulance.html")

#ambulance_call_list secretaire medicale
@app.route("/secretaire_medicales/ambulance_call_list")
@login_required(role='secretaire')
def ambulance_call_list():
    return render_template("secretaire_medicales/gestion_ambulance/ambulance_call_list.html")

#ambulance_list secretaire medicale
@app.route("/secretaire_medicales/ambulance_list")
@login_required(role='secretaire')
def ambulance_list():
    return render_template("secretaire_medicales/gestion_ambulance/ambulance_list.html")


#edit_ambulance secretaire medicale
@app.route("/secretaire_medicales/edit_ambulance")
@login_required(role='secretaire')
def edit_ambulance():
    return render_template("secretaire_medicales/gestion_ambulance/edit_ambulance.html")



#ajouter_patient  secretaire medicale
@app.route("/secretaire_medicales/ajouter_patient")
@login_required(role='secretaire')
def ajouter_patient():
    return render_template("secretaire_medicales/gestion_patients/ajouter_patient.html")



# modifier profile secretaire
@app.route('/secretaire/profile/modifier', methods=['GET', 'POST'])
@login_required(role='secretaire')
def modifier_profile_secretaire():
    if 'email_secretaire' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))

    email = session['email_secretaire']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        donnes = request.form
        nom_utilisateur = donnes.get('username')
        nom = donnes.get('nom')
        prenom = donnes.get('prenom')
        nom_complet = (nom + ' ' + prenom) if nom and prenom else None
        date_naissance = donnes.get('date_naissance')
        sexe = donnes.get('sexe')
        situation_matrimoniale = donnes.get('situation_matrimoniale')
        photo = donnes.get('photo')
        description = donnes.get('description')
        adresse = donnes.get('adresse')
        pays = donnes.get('pays')
        ville = donnes.get('ville')
        code_postal = donnes.get('code_postal')
        numero_telephone = donnes.get('telephone')
        password = donnes.get('new_password')
        confirm_password = donnes.get('confirm_new_password')

        # Horaires semaine
        heure_debut_dimanche = donnes.get('dimanche_debut')
        heure_fin_dimanche = donnes.get('dimanche_fin')
        heure_debut_lundi = donnes.get('lundi_debut')
        heure_fin_lundi = donnes.get('lundi_fin')
        heure_debut_mardi = donnes.get('mardi_debut')
        heure_fin_mardi = donnes.get('mardi_fin')
        heure_debut_mercredi = donnes.get('mercredi_debut')
        heure_fin_mercredi = donnes.get('mercredi_fin')
        heure_debut_jeudi = donnes.get('jeudi_debut')
        heure_fin_jeudi = donnes.get('jeudi_fin')
        heure_debut_vendredi = donnes.get('vendredi_debut')
        heure_fin_vendredi = donnes.get('vendredi_fin')
        heure_debut_samedi = donnes.get('samedi_debut')
        heure_fin_samedi = donnes.get('samedi_fin')

        # Récupérer l'ancien profil
        cursor.execute("SELECT * FROM secretaire_medicale WHERE email_secretaire = %s", (email,))
        ancien_profil = cursor.fetchone()

        if not ancien_profil:
            flash("Profil non trouvé.", "danger")
            cursor.close()
            return redirect(url_for('index_secretaire'))

        # Vérification nom_utilisateur déjà utilisé par un autre compte
        if nom_utilisateur and nom_utilisateur != ancien_profil['nom_utilisateur']:
            cursor.execute("SELECT * FROM secretaire_medicale WHERE nom_utilisateur = %s AND email_secretaire != %s",
                           (nom_utilisateur, email))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Ce nom d'utilisateur est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                cursor.close()
                return redirect(request.url)

        # Gestion du mot de passe
        if password:
            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas. Veuillez réessayer.", "danger")
                cursor.close()
                return redirect(request.url)
            hashed_password = hashlib.md5(password.encode()).hexdigest()
        else:
            hashed_password = ancien_profil['password']

        # Préparer les valeurs en gardant les anciennes si champs vides
        nom_utilisateur = nom_utilisateur or ancien_profil['nom_utilisateur']
        nom_complet = nom_complet or ancien_profil['nom_complet']
        date_naissance = date_naissance or ancien_profil['date_naissance']
        sexe = sexe or ancien_profil['sexe']
        situation_matrimoniale = situation_matrimoniale or ancien_profil['situation_matrimoniale']
        photo = photo or ancien_profil['photo']
        description = description or ancien_profil['description']
        adresse = adresse or ancien_profil['adresse']
        pays = pays or ancien_profil['pays']
        ville = ville or ancien_profil['ville']
        code_postal = code_postal or ancien_profil['code_postal']
        numero_telephone = numero_telephone or ancien_profil['numero_telephone']

        heure_debut_dimanche = heure_debut_dimanche or ancien_profil.get('heure_debut_dimanche')
        heure_fin_dimanche = heure_fin_dimanche or ancien_profil.get('heure_fin_dimanche')
        heure_debut_lundi = heure_debut_lundi or ancien_profil.get('heure_debut_lundi')
        heure_fin_lundi = heure_fin_lundi or ancien_profil.get('heure_fin_lundi')
        heure_debut_mardi = heure_debut_mardi or ancien_profil.get('heure_debut_mardi')
        heure_fin_mardi = heure_fin_mardi or ancien_profil.get('heure_fin_mardi')
        heure_debut_mercredi = heure_debut_mercredi or ancien_profil.get('heure_debut_mercredi')
        heure_fin_mercredi = heure_fin_mercredi or ancien_profil.get('heure_fin_mercredi')
        heure_debut_jeudi = heure_debut_jeudi or ancien_profil.get('heure_debut_jeudi')
        heure_fin_jeudi = heure_fin_jeudi or ancien_profil.get('heure_fin_jeudi')
        heure_debut_vendredi = heure_debut_vendredi or ancien_profil.get('heure_debut_vendredi')
        heure_fin_vendredi = heure_fin_vendredi or ancien_profil.get('heure_fin_vendredi')
        heure_debut_samedi = heure_debut_samedi or ancien_profil.get('heure_debut_samedi')
        heure_fin_samedi = heure_fin_samedi or ancien_profil.get('heure_fin_samedi')

        # Vérification numéro de téléphone
        if numero_telephone == ancien_profil['numero_telephone']:
            pass
        elif numero_telephone and re.match(pattern_phone, numero_telephone):
            pass
        else:
            flash("Numéro de téléphone invalide.", "danger")
            cursor.close()
            return redirect(request.url)

        try:
            cursor.execute("""
                UPDATE secretaire_medicale SET
                    nom_utilisateur=%s,
                    nom_complet=%s,
                    date_naissance=%s,
                    sexe=%s,
                    situation_matrimoniale=%s,
                    photo=%s,
                    description=%s,
                    adresse=%s,
                    pays=%s,
                    ville=%s,
                    code_postal=%s,
                    numero_telephone=%s,
                    password=%s,
                    heure_debut_dimanche=%s,
                    heure_fin_dimanche=%s,
                    heure_debut_lundi=%s,
                    heure_fin_lundi=%s,
                    heure_debut_mardi=%s,
                    heure_fin_mardi=%s,
                    heure_debut_mercredi=%s,
                    heure_fin_mercredi=%s,
                    heure_debut_jeudi=%s,
                    heure_fin_jeudi=%s,
                    heure_debut_vendredi=%s,
                    heure_fin_vendredi=%s,
                    heure_debut_samedi=%s,
                    heure_fin_samedi=%s
                WHERE email_secretaire=%s
            """, (
                nom_utilisateur, nom_complet, date_naissance, sexe,
                situation_matrimoniale, photo, description, adresse,
                pays, ville, code_postal, numero_telephone,
                hashed_password,
                heure_debut_dimanche, heure_fin_dimanche,
                heure_debut_lundi, heure_fin_lundi,
                heure_debut_mardi, heure_fin_mardi,
                heure_debut_mercredi, heure_fin_mercredi,
                heure_debut_jeudi, heure_fin_jeudi,
                heure_debut_vendredi, heure_fin_vendredi,
                heure_debut_samedi, heure_fin_samedi,
                email
            ))
            mysql.connection.commit()
            cursor.close()
            flash("Profil mis à jour avec succès.", "success")
            return redirect(url_for('index_secretaire_medicales'))

        except Exception as e:
            print("Erreur lors de la modification du profil :", e)
            flash("Erreur lors de la modification du profil.", "danger")
            cursor.close()
            return redirect(request.url)

    # GET : Pré-remplir le formulaire
    cursor.execute("SELECT * FROM secretaire_medicale WHERE email_secretaire = %s", (email,))
    secretaire = cursor.fetchone()
    cursor.close()

    # Liste des pays (exemple, adapte si besoin)
    pays = [
        "Afghanistan", "Afrique du Sud", "Albanie", "Algérie", "Allemagne", "Andorre", "Angola", "Antigua-et-Barbuda",
        "Arabie Saoudite", "Argentine", "Arménie", "Australie", "Autriche", "Azerbaïdjan", "Bahamas", "Bahreïn",
        # ... etc
        "France", "Togo", "États-Unis", "Royaume-Uni"
    ]

    return render_template("secretaire_medicales/gestion _secretaire_medical/modifier_profile.html", secretaire=secretaire, pays=pays)

#voir profile secretaire medicale
@app.route("/secretaire_medicales/voir profile")
@login_required(role='secretaire')
def profile_secretaire_medicale():
    return render_template("secretaire_medicales/gestion _secretaire_medical/profile.html")

"""fin secretaire medical"""





"""debut internr medecie"""
@app.route("/interne_medecine")
@login_required(role='interne')
def index_interne_medecine():
    return render_template("interne_medecine/index_interne_medecine.html")


@app.route("/interne_medecine/modifier_profile_interne")
@login_required(role='interne')
def modifier_profile_interne():
    return render_template("interne_medecine/gestion_interne/modiifer_profile.html")
"""fin interne medecie"""


"""debut gestionnaire logistique"""
@app.route("/gestionnaire_logistique")
@login_required(role='logistique')
def index_gestionnaire_logistique():
    return render_template("gestionaire_logistique/index_logistique.html")

@app.route("/gestionnaire_logistique/modifier_profile_logistique")
@login_required(role='logistique')
def modifier_profile_logistique():
    return render_template("gestionaire_logistique/gestion_logistique/modiifer_profile.html")

"""fin gestionnaire de logistique"""



#les connection
#connection de l'admin
def getLogin(session_key, table):
    cur = mysql.connection.cursor()

    loggedIn = False
    firstName = ''

    if session_key in session:
        loggedIn = True

        # Limiter les tables autorisées
        allowed_tables = [
        'admin',
        'doctor',
        'patient',
        'secretaire_medicale',
        'ambulancier',
        'caissier',
        'gestionnaire_logistique',
        'gestionnaire_stock',
        'infirmier',
        'interne_medecine'
    ]
        if table not in allowed_tables:
            raise ValueError("Table non autorisée")

        query = f"SELECT nom_complet FROM {table} WHERE {session_key} = %s"
        cur.execute(query, (session[session_key],))
        result = cur.fetchone()
        if result:
            (firstName,) = result

    cur.close()
    return loggedIn, firstName

# Fonction is_valid

def is_valid(email, email_field, password, table):
    cur = mysql.connection.cursor()

    # Hasher le mot de passe
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    # Sécuriser les noms de table
    allowed_tables = [
        'admin',
        'doctor',
        'patient',
        'secretaire_medicale',
        'ambulancier',
        'caissier',
        'gestionnaire_logistique',
        'gestionnaire_stock',
        'infirmier',
        'interne_medecine'
    ]
    if table not in allowed_tables:
        return False

    # Utiliser une requête paramétrée
    query = f"SELECT * FROM {table} WHERE {email_field} = %s AND password = %s"
    cur.execute(query, (email, hashed_password))
    result = cur.fetchone()
    cur.close()

    return result is not None

"""debut login"""
#fonction login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']
        print(email)
        print(password)

        # Vérification des informations
        if is_valid(email, 'email_admin', password, 'admin'):
            session['email_admin'] = email
            session['role'] = "admin"
            return redirect(url_for('index'))

        elif is_valid(email, "email_doctor", password, "doctor"):

            session['email_doctor'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM doctor WHERE email_doctor = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            # recuperation des donner dans la base de donner
            doctor = Doctor.query.filter_by(email_doctor=email).first()
            session['doctor_id'] = doctor.ident

            if result and result['nom_utilisateur']:# Si rempli
                session['role'] = "doctor"
                return redirect(url_for('index_doctor'))

            else:  # Si vide ou NULL
                session['role'] = "doctor"
                return redirect(url_for('modifier_profile_doctor'))



        elif is_valid(email, "email_patient", password, "patient"):

            session['email_patient'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM patient WHERE email_patient = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            patient = Patient.query.filter_by(email_patient=email).first()

            if patient:

                # Toujours enregistrer patient_id

                session["patient_id"] = patient.ident

                session['role'] = "patient"

                if result and result['nom_utilisateur']:  # Si profil déjà rempli

                    return redirect(url_for('index_patient'))

                else:  # Si profil incomplet

                    return redirect(url_for('modifier_profile_patient'))

            else:

                flash("Patient introuvable.", "danger")

                return redirect(url_for('login_patient'))


        elif is_valid(email, "email_secretaire", password, "secretaire_medicale"):

            session['email_secretaire'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM secretaire_medicale WHERE email_secretaire = %s", (email,))

            result = cursor.fetchone()

            cursor.close()
            secretaire = SecretaireMedicale.query.filter_by(email_secretaire=email).first()
            if result and result['nom_utilisateur']:  # Si rempli
                session["secretaire_id"] = secretaire.ident
                session['role'] = "secretaire"
                return redirect(url_for('index_secretaire_medicales'))

            else:
                session["secretaire_id"] = secretaire.ident
                session['role'] = "secretaire"
                return redirect(url_for('modifier_profile_secretaire'))



        elif is_valid(email, "email_ambulancier", password, "ambulancier"):

            session['email_ambulancier'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM ambulancier WHERE email_ambulancier = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli
                session['role'] = "ambulance"
                return redirect(url_for('index_ambulancier'))

            else:  # Si vide ou NULL
                session['role'] = "ambulance"
                return redirect(url_for('modifier_profile_ambulancier'))



        elif is_valid(email, "email_caissier", password, "caissier"):

            session['email_caissier'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM caissier WHERE email_caissier = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli
                session['role'] = "caissier"
                return redirect(url_for('index_caissier'))

            else:  # Si vide ou NULL
                session['role'] = "caissier"
                return redirect(url_for('modifier_profile_caissier'))



        elif is_valid(email, "email_logistique", password, "gestionnaire_logistique"):

            session['email_logistique'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM gestionnaire_logistique WHERE email_logistique = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli
                session['role'] = "logistique"
                return redirect(url_for('index_logistique'))

            else:  # Si vide ou NULL
                session['role'] = "logistique"
                return redirect(url_for('modifier_profile_logistique'))



        elif is_valid(email, "email_stock", password, "gestionnaire_stock"):

            session['email_stock'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM gestionnaire_stock WHERE email_stock = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli
                session['role'] = "stock"
                return redirect(url_for('index_stock'))

            else:  # Si vide ou NULL
                session['role'] = "stock"
                return redirect(url_for('modifier_profile_stock'))



        elif is_valid(email, "email_infirmier", password, "infirmier"):

            session['email_infirmier'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM infirmier WHERE email_infirmier = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli
                session['role'] = "infirmier"
                return redirect(url_for('index_infirmier'))

            else:  # Si vide ou NULL
                session['role'] = "infirmier"
                return redirect(url_for('modifier_profile_infirmier'))



        elif is_valid(email, "email_interne", password, "interne_medecine"):

            session['email_interne'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM interne_medecine WHERE email_interne = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli
                session['role'] = "interne"
                return redirect(url_for('index_interne'))

            else:  # Si vide ou NULL
                session['role'] = "interne"
                return redirect(url_for('modifier_profile_interne'))

        else:
            flash('Email ou mot de passe incorrect.', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/connexion/login.html')
"""fin login"""



"""debut logout"""
# les deconnection
@app.route('/logout')
@login_required()
def logout():
    # Détection du rôle
    role = None
    nom = session.get('nom', '')

    if 'email_admin' in session:
        role = 'admin'
        session.pop('email_admin')
    elif 'email_doctor' in session:
        role = 'docteur'
        session.pop('email_doctor')
    elif 'email_patient' in session:
        role = 'patient'
        session.pop('email_patient')
    elif 'email_secretaire' in session:
        role = 'secrétaire médicale'
        session.pop('email_secretaire')
    elif 'email_ambulancier' in session:
        role = 'ambulancier'
        session.pop('email_ambulancier')
    elif 'email_caissier' in session:
        role = 'caissier'
        session.pop('email_caissier')
    elif 'email_logistique' in session:
        role = 'gestionnaire logistique'
        session.pop('email_logistique')
    elif 'email_stock' in session:
        role = 'gestionnaire stock'
        session.pop('email_stock')
    elif 'email_infirmier' in session:
        role = 'infirmier'
        session.pop('email_infirmier')
    elif 'email_interne' in session:
        role = 'interne en médecine'
        session.pop('email_interne')

    # Optionnel : vider complètement la session
    session.clear()

    flash(f"Déconnexion de {role or 'utilisateur inconnu'} {nom}", 'success')
    return redirect(url_for('login'))
"""fin logout"""





# les inscription
#systeme denvoie Email
def envoie_email_connection(email, mot_de_passe):

    # ... ici tu enregistres le personnel dans la base de données ...

    # Envoi de l'e-mail automatique
    msg = Message(
        subject="Bienvenue sur notre application",
        recipients=[email],
        body=f"""Bonjour,

            Bienvenue sur MediJutsu ! Votre compte a été créé avec succès. Vous pouvez désormais vous connecter à notre 
            application de gestion hospitalière à l'aide des identifiants suivants :
            
            - Email : {email}
            - Mot de passe : {mot_de_passe}
            
            Merci de votre confiance.
            
            L'équipe de support.
            """
    )
    mail.send(msg)

    return redirect(url_for("index"))  # ou une page de succès

# inscription de l'admininsatrateur
@app.route("/signup_admin", methods=['GET', 'POST'])
@login_required(role='admin')
def signup():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = (donnes.get('name') or '').strip()
            prenom = (donnes.get('prenom') or '').strip()
            nom_complet = name + ' ' + prenom
            email = donnes.get('email')
            numero_telephone = donnes.get('tel')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM admin WHERE email_admin = %s", (email,))
            existing_user = cursor.fetchone()



            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO admin (nom_complet, email_admin, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()
                # Envoi de l'email de confirmation (HTML bien design)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('liste_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "admin")
    else:
        return redirect(url_for('login'))

#inscription du docteur
@app.route("/signup_docteur", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_doctor():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()



            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM doctor WHERE email_doctor = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            # verifier si email est valide
            if re.match(pattern_email, email):
                pass
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:

                cursor.execute("""INSERT INTO doctor (email_doctor, password)
                                VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('liste_docteur_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "doctor")
    else:
        return redirect(url_for('login'))

# #inscription du patient
@app.route("/signup_patient_admin", methods=['GET', 'POST'])
@login_required(role='admin')
def signup_patient_admin():

    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM patient WHERE email_patient = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            # verifier si email est valide
            if re.match(pattern_email, email):
                pass
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)
            try:
                cursor.execute("""INSERT INTO patient (email_patient, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le patient
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('liste_patient_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName,
                               role="patient")
    else:
        return redirect(url_for('login'))


@app.route("/signup_patient", methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        donnes = request.form
        name = (donnes.get('name') or '').strip()
        prenom = (donnes.get('prenom') or '').strip()
        nom_complet = name + ' ' + prenom
        email = donnes.get('email')
        numero_telephone = donnes.get('tel')
        password = donnes.get('pwd')
        confirm_password = donnes.get('conf_pwd')

        if password != confirm_password:
            return "Les mots de passe ne correspondent pas. Veuillez réessayer."

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM patient WHERE email_patient = %s", (email,))
        existing_user = cursor.fetchone()

        # verifier si email est valide
        if re.match(pattern_email, email):
            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)
        else:
            flash("Votre email est invalide", "danger")
            return redirect(request.url)

        # verifier si le numero est valide
        if re.match(pattern_phone, numero_telephone):
            pass
        else:
            flash("phone number invalide", "danger")
            return redirect(request.url)

        try:
            cursor.execute("""INSERT INTO patient (nom_complet, email_patient, numero_telephone, password) 
                              VALUES (%s, %s, %s, %s)""",
                           (nom_complet, email, numero_telephone, hashed_password))

            mysql.connection.commit()

            flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
            return redirect(url_for('index_patient'))

        except Exception as e:

            return f"Erreur lors de l'inscription : {e}"

    return render_template('patient/connexion/signup_patient.html')

# inscription du secretaire medical
@app.route("/signup_secretaire_medical", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_secretaire():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM secretaire_medicale WHERE email_secretaire = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO secretaire_medicale (email_secretaire, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('liste_secretaire_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="secretaire")
    else:
        return redirect(url_for('login'))


@app.route("/signup_ambulancier", methods=['GET', 'POST'])
@login_required(role='admin')
def signup_ambulancier():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM ambulancier WHERE email_ambulancier = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO ambulancier (email_ambulancier, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer l'ambulancier
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="ambulancier")
    else:
        return redirect(url_for('login'))


# inscription du caissier
@app.route("/signup_caissier", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_caissier():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM caissier WHERE email_caissier = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO caissier (email_caissier, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le caissier
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="caissier")
    else:
        return redirect(url_for('login'))


# inscription du gestionnaire_logistique
@app.route("/signup_gestionnaire_logistique", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_logistique():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM gestionnaire_logistique WHERE email_logistique = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO gestionnaire_logistique (email_logistique, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le gestionnaire logistique
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="logistique")
    else:
        return redirect(url_for('login'))


#inscription du gestionnaire_stock
@app.route("/signup_gestionnaire_stock", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_stock():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM gestionnaire_stock WHERE email_stock = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO gestionnaire_stock (email_stock, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le gestionnaire de stock
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="stock")
    else:
        return redirect(url_for('login'))


#inscription du infirmier
@app.route("/signup_infirmier", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_infirmier():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM infirmier WHERE email_infirmier = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO infirmier (email_infirmier, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer l'infirmier
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="infirmier")
    else:
        return redirect(url_for('login'))


#inscription du interne_medecine
@app.route("/signup_interne_medecine", methods=['POST', 'GET'])
@login_required(role='admin')
def signup_interne():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            email = donnes.get('email')
            password = donnes.get('pwd')
            confirm_password = donnes.get('conf_pwd')

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            # Vérifier si l'email est déjà utilisé
            cursor.execute("SELECT * FROM interne_medecine WHERE email_interne = %s", (email,))
            existing_user = cursor.fetchone()

            # verifier si email est valide
            if re.match(pattern_email, email):
                if existing_user:
                    flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                    return redirect(request.url)
            else:
                flash("Votre email est invalide", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO interne_medecine (email_interne, password)
                                  VALUES (%s, %s)""",
                               (email, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer l'interne
                try:
                    envoie_email_connection(email, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role="interne")
    else:
        return redirect(url_for('login'))


"""fin signup"""


"""debut consultation"""
# gestion de conssutation
# ajouter une consultation secretaire medical
@app.route('/secretaire/consultations/nouvelle', methods=['GET', 'POST'])
@login_required(role='secretaire')
def nouvelle_consultation():
    patients = Admission.query.filter(
        (Admission.statut_sortie == "non") | (Admission.statut_sortie.is_(None))
    ).all()
    doctors = Doctor.query.all()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        motif = request.form.get('motif')

        if not patient_id or not doctor_id:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(request.url)

        admission = Admission.query.get(patient_id)

        # 🔹 Récupérer le patient lié via l'email
        patient = Patient.query.filter_by(email_patient=admission.email).first()
        doctor = Doctor.query.get(doctor_id)

        consultation = Consultation(
            patient_id=patient.ident,
            doctor_id=doctor_id,
            date_consultation=datetime.utcnow(),
            etat='en_attente',
            motif=motif,
            poids=admission.poids,
            taille=getattr(admission, 'taille', None),
            temperature=admission.temperature,
            tension_arterielle=admission.tension,
        )

        db.session.add(consultation)
        db.session.flush()

        lier_consultations(consultation.patient_id, consultation)
        db.session.commit()

        # 📩 Envoi email au docteur
        if doctor and doctor.email_doctor:
            msg_doc = Message(
                subject="Nouvelle consultation assignée - MediJustus",
                recipients=[doctor.email_doctor, "elogegomina2@gmail.com"],
                body=f"""
Bonjour Dr {doctor.nom_complet},

Une nouvelle consultation vient de vous être assignée.

🧑 Patient : {patient.nom_complet}
📋 Motif : {motif}
📅 Date : {consultation.date_consultation.strftime('%d/%m/%Y %H:%M')}

Veuillez vous connecter à MediJustus pour plus de détails.
                """
            )
            mail.send(msg_doc)

        # 📩 Envoi email au patient
        if patient and patient.email_patient:
            msg_patient = Message(
                subject="Votre consultation a été enregistrée - MediJustus",
                recipients=[patient.email_patient,"gominaeloge@gmail.com"],
                body=f"""
Bonjour {patient.nom_complet},

Votre consultation a bien été enregistrée.

👨‍⚕️ Médecin assigné : Dr {doctor.nom_complet}
📋 Motif : {motif}
📅 Date : {consultation.date_consultation.strftime('%d/%m/%Y %H:%M')}

Merci de vous présenter pour votre consultation.
                """
            )
            mail.send(msg_patient)

        flash("Consultation enregistrée avec succès ✅ et notifications envoyées 📧", "success")
        return redirect(url_for('liste_consultation_secretaire'))

    return render_template(
        'secretaire_medicales/gestion de consultation/consultation.html',
        patients=patients,
        doctors=doctors
    )

#lier consultation
def lier_consultations(patient_id, nouvelle_consultation):
    # Récupérer la dernière consultation du patient (avant celle-ci)
    precedente = Consultation.query.filter(
        Consultation.patient_id == patient_id,
        Consultation.id != nouvelle_consultation.id  # Éviter de se référencer à soi-même
    ).order_by(Consultation.date_consultation.desc()).first()

    if precedente:
        # Lier les deux consultations
        nouvelle_consultation.consultation_precedente_id = precedente.id
        precedente.consultation_suivante_id = nouvelle_consultation.id
        db.session.add(precedente)  # Nécessaire car on a modifié l'objet


# liste des consultations secretaire
@app.route('/secretaire/consultation/liste')
@login_required(role='secretaire')
def liste_consultation_secretaire():
    # On récupère toutes les consultations, éventuellement triées par date décroissante
    consultations = Consultation.query.order_by(Consultation.date_consultation.desc()).all()

    return render_template(
        'secretaire_medicales/gestion de consultation/liste_consultations.html',
        consultations=consultations
    )

#SUPRIMER CONSULTATION
@app.route("/consultation/supprimer/<int:id>", methods=["GET", "POST"])
def supprimer_consultation(id):
    consultation = Consultation.query.get_or_404(id)

    try:
        db.session.delete(consultation)
        db.session.commit()
        flash("Consultation supprimée avec succès ✅", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erreur lors de la suppression ❌", "danger")
        print(e)

    return redirect(url_for("liste_consultation_secretaire"))

# modifier consultation secretaire
@app.route('/secretaire/consultation/<int:id>/modifier', methods=['GET', 'POST'])
@login_required(role='secretaire')
def modifier_consultation(id):
    consultation = Consultation.query.get_or_404(id)
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == 'POST':
        consultation.patient_id = request.form['patient_id']
        consultation.doctor_id = request.form['doctor_id']
        consultation.motif = request.form.get('motif')
        db.session.commit()
        flash('Consultation modifiée avec succès.', 'success')
        return redirect(url_for('liste_consultation_secretaire'))

    return render_template('secretaire_medicales/gestion de consultation/modifier_consltation.html',
                           consultation=consultation, patients=patients, doctors=doctors)

# historique  consultation secretaire
@app.route('/secretaire/historique_consultations')
@login_required(role='secretaire')
def historique_consultations():
    consultations = Consultation.query.filter(Consultation.etat != None).order_by(Consultation.date_fin_consultation.desc()).all()
    return render_template('secretaire_medicales/gestion de consultation/historique_consultations.html', consultations=consultations)

# voir detail d'une consultation secretaire
@app.route('/secretaire/voir/consultation/<int:id>')
@login_required(role='secretaire')
def voir_consultation_secretaire(id):
    consultation = Consultation.query.get_or_404(id)
    return render_template("doctor/consultation/detail_donsultation.html",
                           consultation=consultation,
                           layout="secretaire_medicales/base_secretaire_medicales.html")

# lisde des consultation medecin
@app.route('/doctor/<int:doctor_id>/consultations')
@login_required(role='doctor')
def liste_consultations_medecin(doctor_id):
    consultations = Consultation.query.filter_by(doctor_id=doctor_id).order_by(Consultation.date_consultation.desc()).all()
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('doctor/consultation/liste_consultation.html', consultations=consultations, doctor=doctor)

# faire consultation medecin
@app.route('/docteur/consultations/<int:consultation_id>/completer', methods=['GET', 'POST'])
@login_required(role='doctor')
def completer_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)

    if request.method == 'POST':
        # Informations générales
        consultation.date_fin_consultation = datetime.utcnow()
        consultation.date_confirmation = datetime.now()
        consultation.etat = "terminee"

        # Motif et plaintes
        consultation.motif = request.form.get('motif')
        consultation.plaintes = request.form.get('plaintes')

        # Antécédents
        consultation.antecedents_personnels = request.form.get('antecedents_personnels')
        consultation.antecedents_familiaux = request.form.get('antecedents_familiaux')
        consultation.allergies = request.form.get('allergies')
        consultation.traitements_en_cours = request.form.get('traitements_en_cours')

        # Examen clinique
        consultation.poids = request.form.get('poids') or None
        consultation.taille = request.form.get('taille') or None
        consultation.temperature = request.form.get('temperature') or None
        consultation.tension_arterielle = request.form.get('tension_arterielle')
        consultation.frequence_cardiaque = request.form.get('frequence_cardiaque') or None
        consultation.frequence_respiratoire = request.form.get('frequence_respiratoire') or None
        consultation.saturation_oxygene = request.form.get('saturation_oxygene') or None
        consultation.observations_cliniques = request.form.get('observations_cliniques')

        # Examens
        consultation.examens_biologiques = request.form.get('examens_biologiques')
        consultation.examens_radiologiques = request.form.get('examens_radiologiques')
        consultation.autres_examens = request.form.get('autres_examens')
        consultation.resultats_examens = request.form.get('resultats_examens')

        # Diagnostic et traitement
        consultation.diagnostic = request.form.get('diagnostic')
        consultation.diagnostic_secondaire = request.form.get('diagnostic_secondaire')
        consultation.traitement = request.form.get('traitement')
        consultation.traitement_non_medic = request.form.get('traitement_non_medic')
        consultation.prescription = request.form.get('prescription')

        # Suivi
        consultation.conseils = request.form.get('conseils')
        prochain_rdv = request.form.get('prochain_rdv')
        consultation.prochain_rdv = datetime.strptime(prochain_rdv, "%Y-%m-%d") if prochain_rdv else None
        consultation.note_suivi = request.form.get('note_suivi')

        # Documents joints (si tu gères des fichiers à part, à adapter)
        consultation.ordonnance_jointe = request.form.get('ordonnance_jointe')  # ou nom de fichier uploadé
        consultation.lettre_orientation = request.form.get('lettre_orientation')
        consultation.documents_scannes = request.form.get('documents_scannes')

        # etat pour la verification
        consultation.etat = "Terminée"
        db.session.commit()
        flash("Consultation complétée avec succès.", "success")
        return redirect(url_for('historique_consultations_doctor', doctor_id=consultation.doctor_id))

    return render_template('doctor/consultation/consultation.html', consultation=consultation)

# consulter consultation medecin
@app.route('/doctor/consultation/historique')
@login_required(role='doctor')
def historique_consultations_doctor():
    doctor_id = session.get('doctor_id')
    consultations = Consultation.query.filter_by(doctor_id=doctor_id).order_by(
        Consultation.date_fin_consultation.desc()
    ).all()

    now = datetime.now()
    consultations_info = []

    for c in consultations:
        modifiable = False
        if c.date_confirmation:
            minutes_passed = (now - c.date_confirmation).total_seconds() / 60
            if minutes_passed <= 5:
                modifiable = True

        consultations_info.append({
            'consultation': c,
            'modifiable': modifiable
        })

    return render_template('doctor/consultation/historique_consultations.html',
                           consultations_info=consultations_info)


# voir consultation passer docteur
@app.route('/doctor/consultation/voir/<int:id>')
@login_required(role='doctor')
def voir_consultation_doctor(id):
    consultation = Consultation.query.get_or_404(id)
    return render_template("doctor/consultation/detail_donsultation.html",
                           consultation=consultation,
                           layout="doctor/base_doctor.html")


#telecharger uyne consltation en pdf
@app.route('/doctor/consultation/<int:id>/telecharger')
@login_required()
def telecharger_consultation(id):
    consultation = Consultation.query.get_or_404(id)
    html = render_template("doctor/consultation/pdf_consultation.html",
                           consultation=consultation,
                           now=datetime.now )

    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    pdf.seek(0)

    return make_response(
        pdf.read(),
        {
            "Content-Type": "application/pdf",
            "Content-Disposition": f"attachment; filename=consultation_{id}.pdf"
        }
    )

# historique des consultation patient
@app.route("/patient/historique_patient/historique_patient")
@login_required(role='patient')
def historique_patient():
    patient_id = session.get('patient_id')  # ID du patient connecté

    if not patient_id:
        flash("Erreur : patient non reconnu.", "danger")
        return redirect(url_for("index_patient"))

    consultations = Consultation.query.filter_by(patient_id=patient_id).order_by(
        Consultation.date_consultation.desc()).all()

    return render_template("patient/historique_patient/historique_patient.html",
                           historique_consultations=consultations)

#detali consumltation patient
@app.route("/patient/consultation/<int:id>")
@login_required(role="patient")
def voir_consultation_patient(id):
    patient_id = session.get("patient_id")

    consultation = Consultation.query.filter_by(id=id, patient_id=patient_id).first()

    if not consultation:
        flash("Consultation introuvable ou accès non autorisé.", "danger")
        return redirect(url_for("historique_patient"))

    return render_template("patient/historique_patient/voir_consultation_patient.html",
                           consultation=consultation)


notifications = [
    {"id": 1, "message": "Rendez-vous confirmé", "lu": False},
    {"id": 2, "message": "Nouveau message du docteur", "lu": False}
]

@app.route("/get_notifications")
def get_notifications():
    notifs = [n for n in notifications if not n["lu"]]
    return jsonify({
        "count": len(notifs),
        "notifications": notifs
    })

@app.route("/mark_as_read/<int:notif_id>")
def mark_as_read(notif_id):
    for n in notifications:
        if n["id"] == notif_id:
            n["lu"] = True
    return jsonify({"status": "ok"})


"""fin consultation"""




#modifier renistaliser mot de pass
@app.route("/Renistialiser_mot_de_passe")
@login_required()
def reset_pasword():
    return render_template("admin/connexion/reset_password.html")

# mot de pass oublier
@app.route("/mot_de_passe_oublié")
@login_required()
def forgot_password():
    return render_template("admin/connexion/forgot_password.html")






















# Ajouter un inventaire
@app.route("/gestionaire_stock/ajout_inventaire")
@login_required(role='admin')
def ajout_inventaire():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    return render_template("gestionaire_stock/gestion_stock/ajout_inventaire.html")


# suppression des inventaire
@app.route("/gestionaire_stock/suppression_inventaire")
@login_required(role='admin')
def suppression_inventaire():
    produits=Produit.query.all()
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    return render_template("gestionaire_stock/gestion_stock/suppression_inventaire.html",   produit=produits[0])

# modifier des inventaire
@app.route("/gestionaire_stock/modification_inventaire")
@login_required(role='admin')
def modification_inventaire():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    return render_template("gestionaire_stock/gestion_stock/suppression_inventaire.html")

# suivi en temps réel
@app.route("/gestionaire_stock/suivi_en_temps_reel")
@login_required(role='admin')
def suivi_en_temps_reel():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    return render_template("gestionaire_stock/gestion_stock/suivi_en_temps_reel.html")

#alerte stock
@app.route("/Module_ia/alerte_stock")
@login_required(role='admin')
def alerte_stock():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    return render_template("gestionaire_stock/Module_ia/alerte_stock.html")

#approvisionement
@app.route("/Module_ia/suggestion_approvisionement")
@login_required(role='admin')
def suggestion_approvisionement():
    if 'email_admin' not in session:
        flash("Connectez-vous d'abord", "warning")
        return redirect(url_for('login'))

    return render_template("gestionaire_stock/Module_ia/suggestion_approvisionement.html")






# gestion de rendez vous
"""debut rendezvous"""

#prendre rendezvous- parient
@app.route('/patient/rendezvous/nouveau', methods=['GET', 'POST'])
@login_required(role='patient')
def nouveau_rendezvous():
    # Récupérer tous les médecins pour le formulaire
    medecins = Doctor.query.all()

    if request.method == 'POST':
        # Récupérer le patient connecté depuis la session
        email_patient = session.get('email_patient')
        patient = Patient.query.filter_by(email_patient=email_patient).first()
        if not patient:
            flash("Patient introuvable.", "danger")
            return redirect(url_for('login'))

        patient_id = patient.ident
        doctor_id = request.form.get('doctor_id') or None
        date_rdv = request.form.get('date_rdv')
        heure_debut = request.form.get('heure_debut')
        heure_fin = request.form.get('heure_fin')
        motif = request.form.get('motif')

        # Vérification des champs
        if not date_rdv or not heure_debut or not heure_fin:
            flash("Veuillez remplir la date et le créneau horaire.", "danger")
            return redirect(url_for('nouveau_rendezvous'))

        # Conversion en objets datetime
        date_rdv_obj = datetime.strptime(date_rdv, "%Y-%m-%d").date()
        heure_debut_obj = datetime.strptime(heure_debut, "%H:%M").time()
        heure_fin_obj = datetime.strptime(heure_fin, "%H:%M").time()

        # Vérifier disponibilité si médecin choisi
        if doctor_id:
            conflict = RendezVous.query.filter_by(doctor_id=doctor_id, date_rdv=date_rdv_obj) \
                .filter(RendezVous.heure_debut < heure_fin_obj) \
                .filter(RendezVous.heure_fin > heure_debut_obj) \
                .first()
            if conflict:
                flash("Ce créneau n'est pas disponible pour ce médecin.", "danger")
                return redirect(url_for('nouveau_rendezvous'))

        # Créer le rendez-vous
        rdv = RendezVous(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date_rdv=date_rdv_obj,
            heure_debut=heure_debut_obj,
            heure_fin=heure_fin_obj,
            motif=motif,
            statut='en attente'
        )
        db.session.add(rdv)
        db.session.commit()

        flash("Rendez-vous enregistré avec succès.", "success")
        return redirect(url_for('calendrier_rendezvous'))

    return render_template('patient/gestion_rendez_vous/nouveau_rendezvous.html', medecins=medecins)

#calendrier rendevous patient
@app.route('/patient/rendezvous/calendrier')
@login_required(role='patient')
def calendrier_rendezvous():
    email_patient = session.get('email_patient')
    patient = Patient.query.filter_by(email_patient=email_patient).first()
    if not patient:
        flash("Patient introuvable.", "danger")
        return redirect(url_for('login'))

    rdvs = RendezVous.query.filter_by(patient_id=patient.ident).all()

    # Préparer les données pour JS
    events = []
    for r in rdvs:
        events.append({
            'date': r.date_rdv.strftime("%Y-%m-%d"),
            'title': f"{r.doctor.nom_complet if r.doctor else 'Médecin non attribué'} - {r.motif}",
            'time': f"{r.heure_debut.strftime('%H:%M')} - {r.heure_fin.strftime('%H:%M')}",
            'statut': r.statut,
            'url': url_for('detail_rendezvous', id=r.id)  # 👈 route vers détail
        })

    return render_template('patient/gestion_rendez_vous/calendrier.html', events=events)

# calendrier des rendezvous docteur
@app.route('/patient/rendezvous/<int:id>')
@login_required(role='patient')
def detail_rendezvous(id):
    rdv = RendezVous.query.get_or_404(id)

    # si tu n’as que rdv.id_medecin
    medecin = Doctor.query.get(rdv.id_medecin) if hasattr(rdv, "id_medecin") else None

    return render_template(
        "patient/gestion_rendez_vous/detail_rendezvous.html",
        rdv=rdv,
        medecin=medecin
    )

#annuler un rendezvous patient
@app.route('/patient/rendezvous/annuler/<int:rendezvous_id>', methods=['POST'])
@login_required(role='patient')
def annuler_rendezvous(rendezvous_id):
    rdv = RendezVous.query.get_or_404(rendezvous_id)

    # Vérification : est-ce bien le patient connecté qui veut annuler ?
    email_patient = session.get('email_patient')
    patient = Patient.query.filter_by(email_patient=email_patient).first()
    if not patient or rdv.patient_id != patient.ident:
        flash("Action non autorisée.", "danger")
        return redirect(url_for('calendrier_rendezvous'))

    # Mettre à jour le statut
    rdv.statut = "annulé"
    db.session.commit()

    flash("Votre rendez-vous a été annulé avec succès.", "success")
    return redirect(url_for('calendrier_rendezvous'))


#doctor rendevous
@app.route("/doctor/rendez-vous")
@login_required(role='doctor')
def rendez_vous_doctor():
    doctor_id = session.get('doctor_id')

    # Rendez-vous du médecin OU rendez-vous non attribués
    rdvs = RendezVous.query.filter(
        (RendezVous.doctor_id == doctor_id) | (RendezVous.doctor_id == None)
    ).all()

    events = []
    for rdv in rdvs:
        title = rdv.patient.nom_complet
        if rdv.doctor_id is None:
            title = (title or "") + " (Non attribué)"

        events.append({
            'date': rdv.date_rdv.strftime("%Y-%m-%d"),
            'time': f"{rdv.heure_debut.strftime('%H:%M')} - {rdv.heure_fin.strftime('%H:%M')}",
            'title': title,
            'statut': rdv.statut,
            'url': url_for('details_rendez_vous_doctor', rdv_id=rdv.id)  # lien vers la vue détail
        })

    return render_template("doctor/gestion_rendezvous/rendezvous.html", events=events)


# detail rendezvous doctor
@app.route("/doctor/rendezvous/<int:rdv_id>/details", methods=["GET", "POST"])
def details_rendez_vous_doctor(rdv_id):
    rdv = RendezVous.query.get_or_404(rdv_id)

    if request.method == "POST":
        action = request.form.get("action")
        doctor_id = session.get("doctor_id")

        #  Attribuer le rdv
        if action == "attribuer" and rdv.doctor_id is None:
            rdv.doctor_id = doctor_id
            rdv.statut = "Confirmé"
            db.session.commit()
            flash("Rendez-vous attribué avec succès.", "success")

            # Notification patient
            envoyer_mail_patient(
                rdv,
                "Votre rendez-vous a été attribué",
                f"Bonjour {rdv.patient.nom_complet},\n\n"
                f"Votre rendez-vous du {rdv.date_rdv} a été accepter par Dr {rdv.doctor.nom_complet}."
            )
            return redirect(url_for("rendez_vous_doctor"))

        #  Confirmer
        if action == "confirmer" and rdv.doctor_id == doctor_id:
            rdv.statut = "Confirmé"
            db.session.commit()
            flash("Rendez-vous confirmé avec succès.", "success")

            #  Mail au patient
            envoyer_mail_patient(
                rdv,
                "Votre rendez-vous est confirmé",
                f"Bonjour {rdv.patient.nom_complet},\n\n"
                f"Votre rendez-vous avec le Dr {rdv.doctor.nom_complet} le {rdv.date_rdv} est confirmé ✅."
            )
            return redirect(url_for("rendez_vous_doctor"))

        #  Annuler
        if action == "attente" and rdv.doctor_id == doctor_id:
            rdv.statut = "Annulé"
            db.session.commit()
            flash("Rendez-vous annulé avec succès.", "success")

            #  Mail au patient
            envoyer_mail_patient(
                rdv,
                "Votre rendez-vous a été annulé",
                f"Bonjour {rdv.patient.nom_complet},\n\n"
                f"Votre rendez-vous avec le Dr {rdv.doctor.nom_complet} prévu le {rdv.date_rdv} a été annulé ❌."
            )
            return redirect(url_for("rendez_vous_doctor"))

        # 🔹 Terminer
        if action == "terminer" and rdv.doctor_id == doctor_id:
            rdv.statut = "Terminé"
            db.session.commit()
            flash("Rendez-vous terminé avec succès.", "success")

            # ✉️ Mail au patient
            envoyer_mail_patient(
                rdv,
                "Votre rendez-vous est terminé",
                f"Bonjour {rdv.patient.nom_complet},\n\n"
                f"Votre rendez-vous avec le Dr {rdv.doctor.nom_complet} du {rdv.date_rdv} est terminé. "
                f"Merci d’avoir utilisé notre service 🙏."
            )
            return redirect(url_for("rendez_vous_doctor"))

    return render_template("doctor/gestion_rendezvous/details_rendezvous.html", rdv=rdv)



#foction pour envyer un mail au patient quand me doctuer confirme ou anule un rendz vous
def envoyer_mail_patient(rdv, sujet, contenu):
    """Fonction utilitaire pour notifier le patient par mail"""
    if rdv.patient and rdv.patient.email_patient:
        msg = Message(
            subject=sujet,
            recipients=[rdv.patient.email_patient,],
            body=contenu
        )
        mail.send(msg)



#prendre rendevous pour le docteur
@app.route("/doctor/rendez-vous/prendre_rendez-vous", methods=['GET', 'POST'])
@login_required(role='doctor')
def prendre_rendez_vous_doctor():
    # Récupérer le docteur connecté depuis la session
    doctor_id = session.get('doctor_id')
    if not doctor_id:
        flash("Docteur non connecté.", "danger")
        return redirect(url_for('login'))

    # Récupérer tous les patients pour le formulaire
    patients = Patient.query.all()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        date_rdv = request.form.get('date_rdv')
        heure_debut = request.form.get('heure_debut')
        heure_fin = request.form.get('heure_fin')
        motif = request.form.get('motif')

        # Vérification des champs obligatoires
        if not patient_id or not date_rdv or not heure_debut or not heure_fin:
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return redirect(url_for('prendre_rendez_vous_doctor'))

        # Conversion en objets datetime
        date_rdv_obj = datetime.strptime(date_rdv, "%Y-%m-%d").date()
        heure_debut_obj = datetime.strptime(heure_debut, "%H:%M").time()
        heure_fin_obj = datetime.strptime(heure_fin, "%H:%M").time()

        # Vérifier disponibilité du médecin
        conflict = RendezVous.query.filter_by(doctor_id=doctor_id, date_rdv=date_rdv_obj) \
            .filter(RendezVous.heure_debut < heure_fin_obj) \
            .filter(RendezVous.heure_fin > heure_debut_obj) \
            .first()
        if conflict:
            flash("Ce créneau n'est pas disponible.", "danger")
            return redirect(url_for('prendre_rendez_vous_doctor'))

        # Créer le rendez-vous attribué au docteur
        rdv = RendezVous(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date_rdv=date_rdv_obj,
            heure_debut=heure_debut_obj,
            heure_fin=heure_fin_obj,
            motif=motif,
            statut='Confirmé'
        )
        db.session.add(rdv)
        db.session.commit()

        # 🔹 Récupérer emails du patient et du docteur
        patient = Patient.query.get(patient_id)
        doctor = Doctor.query.get(doctor_id)

        if patient and doctor:
            try:
                # Préparer l'email au patient
                msg = Message(
                    subject="Confirmation de votre rendez-vous",
                    recipients=[patient.email_patient],  # 📩 email du patient
                    body=f"""Bonjour {patient.nom_complet},

le Dr {doctor.nom_complet} a pris rendezvous avec vous.

📅 Date : {date_rdv_obj.strftime('%d/%m/%Y')}
🕒 Heure : {heure_debut} - {heure_fin}
Motif : {motif}

Merci de vous présenter à l’accueil 10 minutes avant l’heure du rendez-vous.

Cordialement,
L'équipe MediJustsu
"""
                )
                mail.send(msg)
                flash("Rendez-vous attribué et email envoyé au patient.", "success")
            except Exception as e:
                flash(f"Rendez-vous attribué, mais l'email n'a pas pu être envoyé : {str(e)}", "warning")

        return redirect(url_for('rendez_vous_doctor'))

    # Afficher le formulaire
    return render_template(
        "doctor/gestion_rendezvous/prendre_rendezvous.html",
        patients=patients
    )


#modifier rendezvous docreur
@app.route("/doctor/rendez-vous/modifier_rendez-vous/<int:rdv_id>", methods=['GET', 'POST'])
@login_required(role='doctor')
def modifier_rendez_vous_doctor(rdv_id):
    rdv = RendezVous.query.get_or_404(rdv_id)
    if request.method == 'POST':
        rdv.date_rdv = request.form.get('date_rdv')
        rdv.heure_debut = request.form.get('heure_debut')
        rdv.heure_fin = request.form.get('heure_fin')
        rdv.motif = request.form.get('motif')
        db.session.commit()
        flash("Rendez-vous modifié avec succès", "success")
        return redirect(url_for('rendez_vous_doctor'))

    return render_template("doctor/gestion_rendezvous/modifier_rendezvous.html", rdv=rdv)



#gestion_rendezvous secretaire medicale
@app.route("/secretaire/rendez-vous", methods=['GET'])
@login_required(role='secretaire')
def calendrier_rendezvous_secretaire():
    # Récupérer tous les rendez-vous
    rdvs = RendezVous.query.all()

    # Transformer en liste d'événements pour le calendrier JS
    events = []
    for rdv in rdvs:
        events.append({
            'title': f"{rdv.patient.nom_complet} / {rdv.doctor.nom_complet if rdv.doctor else 'Non attribué'}",
            'date': rdv.date_rdv.strftime("%Y-%m-%d"),
            'time': f"{rdv.heure_debut.strftime('%H:%M')} - {rdv.heure_fin.strftime('%H:%M')}",
            'statut': rdv.statut,
            'url': url_for('details_rendez_vous_secretaire', rdv_id=rdv.id)
        })

    return render_template(
        "secretaire_medicales/gestion_rendez_vous/calendrier_rendezvous.html",
        events=events
    )


@app.route("/secretaire/rendezvous/<int:rdv_id>/details", methods=["GET", "POST"])
@login_required(role='secretaire')
def details_rendez_vous_secretaire(rdv_id):
    rdv = RendezVous.query.get_or_404(rdv_id)
    medecins = Doctor.query.all()

    if request.method == "POST":
        action = request.form.get("action")
        patient = Patient.query.get(rdv.patient_id)
        doctor = Doctor.query.get(rdv.doctor_id) if rdv.doctor_id else None

        # Attribuer un médecin
        if action == "attribuer_medecin":
            selected_medecin_id = request.form.get("doctor_id")
            if selected_medecin_id:
                rdv.doctor_id = int(selected_medecin_id)
                rdv.statut = "Confirmé"
                rdv.secretaire_id = session.get("secretaire_id")
                db.session.commit()

                # Envoyer email de confirmation après attribution
                envoyer_email_rendezvous(
                    destinataire=patient.email_patient,
                    nom=patient.nom_complet,
                    date_rdv=rdv.date_rdv,
                    heure_debut=rdv.heure_debut,
                    heure_fin=rdv.heure_fin,
                    motif=rdv.motif,
                    role="patient",
                    medecin_nom=Doctor.query.get(selected_medecin_id).nom_complet
                )
                doctor = Doctor.query.get(selected_medecin_id)
                envoyer_email_rendezvous(
                    destinataire=doctor.email_doctor,
                    nom=doctor.nom_complet,
                    date_rdv=rdv.date_rdv,
                    heure_debut=rdv.heure_debut,
                    heure_fin=rdv.heure_fin,
                    motif=rdv.motif,
                    role="docteur",
                    patient_nom=f"{patient.nom_complet}"
                )

                flash("Médecin attribué et notifications envoyées.", "success")
            else:
                flash("Veuillez sélectionner un médecin.", "warning")
            return redirect(url_for("calendrier_rendezvous_secretaire"))

        # Confirmer un rendez-vous
        elif action == "confirmer" and rdv.statut.lower() == "en attente" and rdv.doctor_id:
            rdv.statut = "Confirmé"
            rdv.secretaire_id = session.get("secretaire_id")
            db.session.commit()

            # Envoyer notifications
            envoyer_email_rendezvous(
                destinataire=patient.email_patient,
                nom=patient.nom_complet,
                date_rdv=rdv.date_rdv,
                heure_debut=rdv.heure_debut,
                heure_fin=rdv.heure_fin,
                motif=rdv.motif,
                role="patient",
                medecin_nom=doctor.nom_complet if doctor else "Non attribué"
            )
            if doctor:
                envoyer_email_rendezvous(
                    destinataire=doctor.email_doctor,
                    nom=doctor.nom_complet,
                    date_rdv=rdv.date_rdv,
                    heure_debut=rdv.heure_debut,
                    heure_fin=rdv.heure_fin,
                    motif=rdv.motif,
                    role="docteur",
                    patient_nom=f"{patient.nom_complet}"
                )

            flash("Rendez-vous confirmé et notifications envoyées.", "success")
            return redirect(url_for("calendrier_rendezvous_secretaire"))

        # Mettre en attente
        elif action == "attente":
            rdv.statut = "En attente"
            rdv.secretaire_id = session.get("secretaire_id")
            db.session.commit()
            flash("Rendez-vous mis en attente.", "warning")
            return redirect(url_for("calendrier_rendezvous_secretaire"))

        # Annuler
        elif action == "annuler":
            rdv.statut = "Annulé"
            rdv.secretaire_id = session.get("secretaire_id")
            db.session.commit()

            # Envoyer email d’annulation
            envoyer_email_rendezvous(
                destinataire=patient.email_patient,
                nom=patient.nom_complet,
                date_rdv=rdv.date_rdv,
                heure_debut=rdv.heure_debut,
                heure_fin=rdv.heure_fin,
                motif=rdv.motif,
                role="patient",
                annulation=True
            )
            if doctor:
                envoyer_email_rendezvous(
                    destinataire=doctor.email_doctor,
                    nom=doctor.nom_complet,
                    date_rdv=rdv.date_rdv,
                    heure_debut=rdv.heure_debut,
                    heure_fin=rdv.heure_fin,
                    motif=rdv.motif,
                    role="docteur",
                    patient_nom=f"{patient.nom_complet}",
                    annulation=True
                )

            flash("Rendez-vous annulé et notifications envoyées.", "danger")
            return redirect(url_for("calendrier_rendezvous_secretaire"))

        # Terminer
        elif action == "terminer":
            rdv.statut = "Terminé"
            rdv.secretaire_id = session.get("secretaire_id")
            db.session.commit()
            flash("Rendez-vous terminé.", "success")
            return redirect(url_for("calendrier_rendezvous_secretaire"))

    return render_template(
        "secretaire_medicales/gestion_rendez_vous/details_rendezvous.html",
        rdv=rdv,
        medecins=medecins
    )





#prendre_rendezvous secretaire medicale
@app.route("/secretaire/rendez-vous/nouveau", methods=['GET', 'POST'])
@login_required(role='secretaire')
def prendre_rendez_vous_secretaire():
    patients = Patient.query.all()
    medecins = Doctor.query.all()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id') or None
        doctor_id = request.form.get('doctor_id') or None
        date_rdv = request.form.get('date_rdv')
        heure_debut = request.form.get('heure_debut')
        heure_fin = request.form.get('heure_fin')
        motif = request.form.get('motif')

        if not patient_id or not date_rdv or not heure_debut or not heure_fin:
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return redirect(url_for('prendre_rendez_vous_secretaire'))

        # Conversion des dates/heures
        date_rdv_obj = datetime.strptime(date_rdv, "%Y-%m-%d").date()
        heure_debut_obj = datetime.strptime(heure_debut, "%H:%M").time()
        heure_fin_obj = datetime.strptime(heure_fin, "%H:%M").time()

        # Vérifier disponibilité du médecin
        if doctor_id:
            conflict = RendezVous.query.filter_by(doctor_id=doctor_id, date_rdv=date_rdv_obj) \
                .filter(RendezVous.heure_debut < heure_fin_obj) \
                .filter(RendezVous.heure_fin > heure_debut_obj) \
                .first()
            if conflict:
                flash("Ce créneau n'est pas disponible pour ce médecin.", "danger")
                return redirect(url_for('prendre_rendez_vous_secretaire'))

        # Création du rendez-vous
        rdv = RendezVous(
            patient_id=patient_id,
            doctor_id=doctor_id,
            secretaire_id=session.get("secretaire_id"),
            date_rdv=date_rdv_obj,
            heure_debut=heure_debut_obj,
            heure_fin=heure_fin_obj,
            motif=motif,
            statut='confirmé' if doctor_id else 'En attente'
        )
        db.session.add(rdv)
        db.session.commit()

        # Récupérer infos patient et médecin
        patient = Patient.query.get(patient_id)
        doctor = Doctor.query.get(doctor_id) if doctor_id else None

        # Envoi d'email au patient
        envoyer_email_rendezvous(
            destinataire=patient.email_patient,
            nom=patient.nom_complet,
            date_rdv=date_rdv,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            motif=motif,
            role="patient",
            medecin_nom=doctor.nom_complet if doctor else "Non encore attribué"
        )

        # Envoi d'email au médecin (si choisi)
        if doctor:
            envoyer_email_rendezvous(
                destinataire=doctor.email_doctor,
                nom=doctor.nom_complet,
                date_rdv=date_rdv,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                motif=motif,
                role="docteur",
                patient_nom=f"{patient.nom_complet}"
            )

        flash("Rendez-vous créé avec succès et notifications envoyées.", "success")
        return redirect(url_for('calendrier_rendezvous_secretaire'))

    return render_template(
        "secretaire_medicales/gestion_rendez_vous/prendre_rendezvous.html",
        patients=patients,
        medecins=medecins
    )


def envoyer_email_rendezvous(destinataire, nom, date_rdv, heure_debut, heure_fin, motif, role, medecin_nom=None, patient_nom=None, annulation=False):
    if annulation:
        if role == "patient":
            body = f"""
            Bonjour {nom},

            ❌ Votre rendez-vous prévu le {date_rdv} de {heure_debut} à {heure_fin} 
            a été ANNULÉ.

            Motif : {motif}

            Merci de reprendre contact avec la secrétaire pour reprogrammer.
            """
        else:  # Médecin
            body = f"""
            Bonjour Dr. {nom},

            ❌ Le rendez-vous avec le patient {patient_nom}, prévu le {date_rdv} de {heure_debut} à {heure_fin},
            a été ANNULÉ.

            Motif : {motif}
            """
    else:
        if role == "patient":
            body = f"""
            Bonjour {nom},

            ✅ Votre rendez-vous est CONFIRMÉ :
            - Date : {date_rdv}
            - Heure : {heure_debut} à {heure_fin}
            - Médecin : {medecin_nom}
            - Motif : {motif}

            Merci de vous présenter 10 minutes à l’avance.
            """
        else:  # Médecin
            body = f"""
            Bonjour Dr. {nom},

            ✅ Un rendez-vous vous a été attribué :
            - Date : {date_rdv}
            - Heure : {heure_debut} à {heure_fin}
            - Patient : {patient_nom}
            - Motif : {motif}
            """

    msg = Message(
        subject="Notification Rendez-vous - MediJustus",
        recipients=[destinataire],
        body=body
    )
    mail.send(msg)

"""fin rendezvous"""




#dossier medicale
"""gestion dossier medicale"""
#dossiermedicla patient
@app.route("/patient/dossier_medical/<int:patient_id>")
@login_required(role='patient')
def dossier_medical_patient(patient_id):
    # 🔹 Récupérer le patient
    patient = Patient.query.get_or_404(patient_id)

    # 🔹 Récupérer ses consultations
    consultations = Consultation.query.filter_by(patient_id=patient.ident).all()

    # 🔹 Récupérer ses rendez-vous
    rendezvous = RendezVous.query.filter_by(patient_id=patient.ident).all()

    # 🔹 Récupérer ses admissions et sorties
    admissions = Admission.query.filter_by(email=patient.email_patient).all()
    sorties = Sortie.query.join(Admission).filter(Admission.email == patient.email_patient).all()

    return render_template(
        "patient/gestion_dossier_medical/dossier_medical.html",
        patient=patient,
        consultations=consultations,
        rendezvous=rendezvous,
        admissions=admissions,
        sorties=sorties
    )

#dossier medical parient docteur
@app.route("/doctor/dossier_patient/<int:patient_id>")
@login_required(role="doctor")
def dossier_patient_docteur(patient_id):
    # Récupère le patient
    patient = Patient.query.get_or_404(patient_id)

    # Utilisation de l'email pour lier les admissions et sorties
    admissions = Admission.query.filter_by(email=patient.email_patient).all()
    sorties = Sortie.query.filter_by(email=patient.email_patient).all()

    # Consultations et rendez-vous liés par patient_id
    consultations = Consultation.query.filter_by(patient_id=patient.ident).all()
    rendezvous = RendezVous.query.filter_by(patient_id=patient.ident).all()

    return render_template(
        "doctor/dossier_medical/dossier_medical.html",
        patient=patient,
        admissions=admissions,
        sorties=sorties,
        consultations=consultations,
        rendezvous=rendezvous,
    )



@app.route("/doctor/liste/patients")
@login_required(role="doctor")
def liste_patients_dossier_medical():
    patients = Patient.query.all()
    return render_template("doctor/dossier_medical/liste_patients.html", patients=patients)



if __name__ == "__main__":
    app.run(debug=True)


# Afficher toutes les ressources
@app.route("/ressources")
@login_required(role='admin')
def liste_ressources():
    
    return render_template("logistique/ressources/liste.html", )

# Enregistrer une ressource
@app.route("/ressources/ajouter", methods=["GET", "POST"])
@login_required(role='admin')
def ajouter_ressource():
    
    return render_template("logistique/ressources/ajouter.html")

# Modifier une ressource
@app.route("/ressources/modifier/<int:id>", methods=["GET", "POST"])
@login_required(role='admin')
def modifier_ressource(id):
   
    return render_template("logistique/ressources/modifier.html", )

# Supprimer une ressource
@app.route("/ressources/supprimer/<int:id>")
@login_required(role='admin')
def supprimer_ressource(id):
    
    return redirect(url_for("logistique.liste_ressources"))



@app.route("/equipements")
@login_required(role='admin')
def liste_equipements():
    
    return render_template("logistique/equipements/liste.html")

@app.route("/equipements/suivi/<int:id>")
@login_required(role='admin')
def suivi_equipement(id):
    
    return render_template("logistique/equipements/suivi.html")



@app.route("/maintenance/ajouter/<int:equipement_id>", methods=["GET", "POST"])
@login_required(role='admin')
def ajouter_maintenance(equipement_id):
       
    return render_template("logistique/maintenance/ajouter.html")

@app.route("/maintenance/supprimer/<int:id>")
@login_required(role='admin')

def supprimer_maintenance(id):
   
    return redirect(url_for("logistique.suivi_equipement"))
