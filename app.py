from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
from credentials import *
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# pour la base de donner
app.config['SECRET_KEY']=my_token
app.config['MYSQL_HOST'] = my_host
app.config['MYSQL_USER'] = my_user
app.config['MYSQL_PASSWORD'] = my_password
app.config['MYSQL_DB'] =  my_db
app.config['MYSQL_CURSORCLASS'] =my_CURSORCLASS


#pour l'envoie de Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = my_email
app.config['MAIL_PASSWORD'] = my_password_generer
app.config['MAIL_DEFAULT_SENDER'] = ('Flask', 'elogegomina@gmail.com')

mail = Mail(app)

mysql = MySQL()
mysql.init_app(app)

app.secret_key = my_secret_key
@app.route("/admin")
def index():
    return render_template("admin/index_admin.html")

@app.route("/ambulance")
def index_ambulance():
    return render_template("ambulance/index_ambulance.html")

@app.route("/caissier")
def index_caissier():
    return render_template("caissier/index_caissier.html")

# docteur
@app.route("/doctor")
def index_doctor():
    return render_template("doctor/index_doctor.html")

@app.route("/doctor/liste_doctor")
def liste_doctor():
    return render_template("doctor/gestion_docteur/liste_doctor.html")

@app.route("/doctor/doctor/modifier_profile", methods=['GET', 'POST'])
def modifier_profile_doctor():
    if 'email_doctor' not in session:
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('login'))

    email = session['email_doctor']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        donnes = request.form
        nom_utilisateur = donnes.get('nom_utilisateur')
        nom = donnes.get('nom')
        prenom = donnes.get('prenom')
        nom_complet = nom + ' ' + prenom
        date_naissance = donnes.get('date_naissance')
        sexe = donnes.get('sexe')
        situation_matrimoniale = donnes.get('situation_matrimoniale')
        groupe_sanguin = donnes.get('groupe_sanguin')
        photo = donnes.get('photo')
        description = donnes.get('description')
        adresse = donnes.get('adresse')
        pays = donnes.get('pays')
        ville = donnes.get('ville')
        code_postal = donnes.get('code_postal')
        numero_telephone = donnes.get('numero_telephone')
        qualification = donnes.get('qualification')
        designation = donnes.get('designation')

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
                designation=%s
            WHERE email_doctor=%s
        """, (
            nom_utilisateur, nom_complet, date_naissance, sexe,
            situation_matrimoniale, groupe_sanguin, photo, description,
            adresse, pays, ville, code_postal, numero_telephone,
            qualification, designation, email
        ))

        mysql.connection.commit()
        cursor.close()
        flash("Profil mis à jour avec succès.", "success")
        return redirect(url_for('index_doctor'))

    # En GET : Pré-remplir les champs
    cursor.execute("SELECT * FROM doctor WHERE email_doctor = %s", (email,))
    doctor = cursor.fetchone()
    cursor.close()

    return render_template("doctor/gestion_docteur/modifier_profile.html", doctor=doctor)

@app.route("/doctor/profile_doctor")
def profile_doctor():
    return render_template("doctor/gestion_docteur/profile_doctor.html")

#doctor patient
@app.route("/doctor/liste_patient")
def liste_patient_doctor():
    return render_template("doctor/gestion_patient/liste_patient.html")

@app.route("/doctor/ajout_patient")
def add_patient_doctor():
    return render_template("doctor/gestion_patient/ajout_patient.html")

@app.route("/doctor/modifier_patient")
def modifier_patient_doctor():
    return render_template("doctor/gestion_patient/modifier_patient.html")

#doctor rendevous
@app.route("/doctor/rendez-vous")
def rendez_vous_doctor():
    return render_template("doctor/gestion_rendezvous/rendezvous.html")

@app.route("/doctor/rendez-vous/prendre_rendez-vous")
def prendre_rendez_vous_doctor():
    return render_template("doctor/gestion_rendezvous/prendre_rendezvous.html")

@app.route("/doctor/rendez-vous/modifier_rendez-vous")
def modifier_rendez_vous_doctor():
    return render_template("doctor/gestion_rendezvous/modifier_rendezvous.html")

@app.route("/doctor/rendez-vous/liste_rendez-vous")
def liste_rendez_vous_doctor():
    return render_template("doctor/gestion_rendezvous/liste_rendevous.html")

#doctor conge presence
@app.route("/doctor/conge_presence/congé")
def conge_doctor():
    return render_template("doctor/conge_presence/conge.html")

@app.route("/doctor/conge_presence/présence")
def presence_doctor():
    return render_template("doctor/conge_presence/presence.html")

# doctor galeri et evenement
@app.route("/doctor/actualiter")
def actualiter_doctor():
    return render_template("doctor/galerie_&_evenement/actualiter.html")

@app.route("/doctor/evenement")
def evenement_doctor():
    return render_template("doctor/galerie_&_evenement/evenement.html")

@app.route("/doctor/galerie")
def galerie_doctor():
    return render_template("doctor/galerie_&_evenement/galerie.html")

# doctor ia
@app.route("/doctor/ia/resumer_dossier_medical")
def resumer_dossier_doctor():
    return render_template("doctor/gestion_ia/resumer_dossier.html")

@app.route("/doctor/ia/sugection_de_traitement")
def sugetion_doctor():
    return render_template("doctor/gestion_ia/sugection_traitement.html")

@app.route("/doctor/ia/surleillance_patient")
def surveillance_dossier_doctor():
    return render_template("doctor/gestion_ia/survellanc_patient.html")

# doctor messagerie
@app.route("/doctor/messagerie")
def messageire_doctor():
    return render_template("doctor/gestion_messagerie/messagerie.html")

#doctor hospitalisation
@app.route("/doctor/hospitalisation")
def hospitalisation_doctor():
    return render_template("doctor/hospitalisation/hospitalisation.html")

#parametre dcoctor
@app.route("/doctor/parametre")
def parametre_doctor():
    return render_template("doctor/parametre/parametre.html")

# fiche de paie doctor
@app.route("/doctor/salaire/fiche_de_paie")
def fiche_de_paie_doctor():
    return render_template("doctor/salaire/fiche_de_paie.html")

# dossiermedical doctor
@app.route("/doctor/dossier_medical")
def dossier_medical_doctor():
    return render_template("doctor/dossier_medical/dossier_medical.html")

# consultation
@app.route("/doctor/consultation")
def consultation_doctor():
    return render_template("doctor/consultation/consultation.html")






#gestonaire de stoCK
@app.route("/gestionaire_stock")
def index_gestionaire_stock():
    return render_template("gestionaire_stock/index_gestionaire_stock.html")

@app.route("/infirmier")
def index_infirmier():
    return render_template("infirmier/index_infirmier.html")

@app.route("/patient")
def index_patient():
    return render_template("patient/index_patient.html")

@app.route("/secretaire_medicales")
def index_secretaire_medicales():
    return render_template("secretaire_medicales/index_secretaire_medicales.html")

@app.route("/interne_medecine")
def index_interne_medecine():
    return render_template("interne_medecine/index_interne_medecine.html")

@app.route("/gestionnaire_logistique")
def index_gestionnaire_logistique():
    return render_template("gestionaire_logistique/index_logistique.html")

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
            return redirect(url_for('index'))

        elif is_valid(email, "email_doctor", password, "doctor"):

            session['email_doctor'] = email

            # Connexion à la base

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("SELECT nom_utilisateur FROM doctor WHERE email_doctor = %s", (email,))

            result = cursor.fetchone()

            cursor.close()

            if result and result['nom_utilisateur']:  # Si rempli

                return redirect(url_for('index_doctor'))

            else:  # Si vide ou NULL

                return redirect(url_for('modifier_profile_doctor'))

        elif is_valid(email, "email_patient", password, "patient"):
            session['email_patient'] = email
            return redirect(url_for('index_patient'))

        elif is_valid(email, "email_secretaire", password, "secretaire_medicale"):
            session['email_secretaire'] = email
            return redirect(url_for('index_secretaire'))

        elif is_valid(email, "email_ambulancier", password, "ambulancier"):
            session['email_ambulancier'] = email
            return redirect(url_for('index_ambulancier'))

        elif is_valid(email, "email_caissier", password, "caissier"):
            session['email_caissier'] = email
            return redirect(url_for('index_caissier'))

        elif is_valid(email, "email_logistique", password, "gestionnaire_logistique"):
            session['email_logistique'] = email
            return redirect(url_for('index_logistique'))

        elif is_valid(email, "email_stock", password, "gestionnaire_stock"):
            session['email_stock'] = email
            return redirect(url_for('index_stock'))

        elif is_valid(email, "email_infirmier", password, "infirmier"):
            session['email_infirmier'] = email
            return redirect(url_for('index_infirmier'))

        elif is_valid(email, "email_interne", password, "interne_medecine"):
            session['email_interne'] = email
            return redirect(url_for('index_interne'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/connexion/login.html')

"""
# connection du patient
@app.route("/login_patient", methods = ["POST", "GET"])
def login_patient():
    def recherche_utilisateur(email_utilisateur, mot_pass):
        cur = mysql.connection.cursor()
        cur.execute("SELECT email_patient, password, nom_complet FROM patient")
        lignes = cur.fetchall()
        cur.close()
        mot_pass_hash = hashlib.md5(mot_pass.encode()).hexdigest()
        for ligne in lignes:
            if ligne[0] == email_utilisateur and ligne[1] == mot_pass_hash:
                return ligne
        return None

    #traitement de donnés
    if request.method == "POST":
        donnes_patient = request.form
        email = donnes_patient.get('email')
        pwd = donnes_patient.get('pwd')

        utilisateur = recherche_utilisateur(email, pwd)

        if utilisateur is not None:
            print("utilisateur trouvé")
            session['email_utilisateur'] = utilisateur[0]
            session['nom'] = utilisateur[2]
            print(session)
            flash("utilisateur trouver connection", "success")
            return redirect(url_for('index_patient'))
        else:
            print('utilisateur inconue')
            print(email , pwd)
            flash("Utilusateur inconnu", "danger")
            return redirect(request.url)
    #si l'utilisateur est deja connecter a une session
    else:
        if  'email_utilisateur' in session:
            print(session)
            return redirect(url_for('index_patient'))
        return render_template("admin/login.html", role = 'patient')
"""

# les deconnection
@app.route('/logout')
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



# les inscription
#systeme denvoie Email
def envoie_email_connection(email, nom, mot_de_passe):

    # ... ici tu enregistres le personnel dans la base de données ...

    # Envoi de l'e-mail automatique
    msg = Message(
        subject="Bienvenue sur notre application",
        recipients=[email],
        body=f"""Bonjour {nom},

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
def signup():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO admin (nom_complet, email_admin, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()
                # Envoi de l'email de confirmation (HTML bien design)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('login'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "admin")
    else:
        return redirect(url_for('login'))

#inscription du docteur
@app.route("/signup_docteur", methods=['POST', 'GET'])
def signup_doctor():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM doctor WHERE email_doctor = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:

                cursor.execute("""INSERT INTO doctor (nom_complet, email_doctor, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "doctor")
    else:
        return redirect(url_for('login'))

# #inscription du patient
@app.route("/signup_patient_admin", methods=['GET', 'POST'])
def signup_patient_admin():
    if request.method == 'POST':
        name = request.form['name']
        prenom = request.form['prenom']
        nom_complet = name + ' ' + prenom
        email = request.form['email']
        numero_telephone = request.form['tel']
        password = request.form['pwd']
        confirm_password = request.form['conf_pwd']

        if password != confirm_password:
            return "Les mots de passe ne correspondent pas. Veuillez réessayer."

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM patient WHERE email_patient = %s", (email,))
        existing_user = cursor.fetchone()


        if existing_user:
            flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
            return redirect(request.url)

        try:
            cursor.execute("""INSERT INTO patient (nom_complet, email_patient, numero_telephone, password) 
                            VALUES (%s, %s, %s, %s)""",
                           (nom_complet, email, numero_telephone, hashed_password))

            mysql.connection.commit()

            # Envoi de l'email pour informer le personnel
            try:
                envoie_email_connection(email, nom_complet, password)
            except Exception as e:
                print(e)

            flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
            return redirect(url_for('index'))

        except Exception as e:

            return f"Erreur lors de l'inscription : {e}"

    return render_template('admin/connexion/signup.html', role = "patient")

@app.route("/signup_patient", methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        name = request.form['name']
        prenom = request.form['prenom']
        nom_complet = name + ' ' + prenom
        email = request.form['email']
        numero_telephone = request.form['tel']
        password = request.form['pwd']
        confirm_password = request.form['conf_pwd']

        if password != confirm_password:
            return "Les mots de passe ne correspondent pas. Veuillez réessayer."

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM patient WHERE email_patient = %s", (email,))
        existing_user = cursor.fetchone()


        if existing_user:
            flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
            return redirect(request.url)

        try:
            cursor.execute("""INSERT INTO patient (nom_complet, email_patient, numero_telephone, password) 
                            VALUES (%s, %s, %s, %s)""",
                           (nom_complet, email, numero_telephone, hashed_password))

            mysql.connection.commit()
            # Envoi de l'email de confirmation (HTML bien design)

            flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
            return redirect(url_for('index_patient'))

        except Exception as e:

            return f"Erreur lors de l'inscription : {e}"

    return render_template('patient/connexion/signup_patient.html')

# inscription du secretaire medical
@app.route("/signup_secretaire_medical", methods=['POST', 'GET'])
def signup_secretaire():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM secretaire_medicale WHERE email_secretaire = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO secretaire_medicale (nom_complet, email_secretaire, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "secretaire")
    else:
        return redirect(url_for('login'))

# inscription du ambulancier
@app.route("/signup_ambulancier", methods=['POST', 'GET'])
def signup_ambulancier():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM ambulancier WHERE email_ambulancier = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO ambulancier (nom_complet, email_ambulancier, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "ambulancier")
    else:
        return redirect(url_for('login'))

# inscription du caissier
@app.route("/signup_ambulancier", methods=['POST', 'GET'])
def signup_caissier():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM caissier WHERE email_caissier = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO caissier (nom_complet, email_caissier, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "caissier")
    else:
        return redirect(url_for('login'))

# inscription du gestionnaire_logistique
@app.route("/signup_gestionnaire_logistique", methods=['POST', 'GET'])
def signup_logistique():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM gestionnaire_logistique WHERE email_logistique = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO gestionnaire_logistique (nom_complet, email_logistique, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index_admin'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "logistique")
    else:
        return redirect(url_for('login'))

#inscription du gestionnaire_stock
@app.route("/signup_gestionnaire_stock", methods=['POST', 'GET'])
def signup_stock():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM gestionnaire_stock WHERE email_stock = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO gestionnaire_stock (nom_complet, email_stock, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "stock")
    else:
        return redirect(url_for('login'))

#inscription du infirmier
@app.route("/signup_infirmier", methods=['POST', 'GET'])
def signup_infirmier():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM infirmier WHERE email_infirmier = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO infirmier (nom_complet, email_infirmier, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for('index'))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "infirmier")
    else:
        return redirect(url_for('login'))

#inscription du interne_medecine
@app.route("/signup_infirmier", methods=['POST', 'GET'])
def signup_interne():
    if 'email_admin' in session:
        loggedIn, firstName = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            donnes = request.form
            name = donnes.get('name')
            prenom = donnes.get('prenom')
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
            cursor.execute("SELECT * FROM interne_medecine WHERE email_interne = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect(request.url)

            try:
                cursor.execute("""INSERT INTO interne_medecine (nom_complet, email_interne, numero_telephone, password)
                                VALUES (%s, %s, %s, %s)""",
                               (nom_complet, email, numero_telephone, hashed_password))
                mysql.connection.commit()

                # Envoi de l'email pour informer le personnel
                try:
                    envoie_email_connection(email, nom_complet, password)
                except Exception as e:
                    print(e)

                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect(url_for(''))

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/signup.html', loggedIn=loggedIn, firstName=firstName, role = "interne")
    else:
        return redirect(url_for('login'))





#modifier renistaliser mot de pass
@app.route("/Renistialiser_mot_de_passe")
def reset_pasword():
    return render_template("admin/connexion/reset_password.html")

# mot de pass oublier
@app.route("/mot_de_passe_oublié")
def forgot_password():
    return render_template("admin/connexion/forgot_password.html")



@app.route("/list_patient")
def list_patient():
    return render_template("admin/liste_des_utilisateur/list_patient.html")

@app.route("/list_doctor")
def list_doctor():
    return  render_template("admin/liste_des_utilisateur/list_doctor.html")

@app.route("/list_admin")
def list_admin():
    return  render_template("admin/liste_des_utilisateur/list_admin.html")

@app.route("/list_personnel")
def list_personnel():
    return  render_template("admin/liste_des_utilisateur/list_personnel.html")


if __name__ == "__main__":
    app.run(debug=True)