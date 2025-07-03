@app.route("/creer_compte_admin", methods=['GET', 'POST'])
def creer_compte_admin():
    if 'email_admin' in session:
        loggedIn, firstName, userEmail = getLogin('email_admin', 'admin')
        if request.method == 'POST':
            name = request.form['name']
            prenom = request.form['prenom']
            nom_complet = name + ' ' + prenom
            email = request.form['email_admin']
            sexe = request.form['sexe']
            numero_telephone = request.form['numero_telephone']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                return "Les mots de passe ne correspondent pas. Veuillez réessayer."

            hashed_password = hashlib.md5(password.encode()).hexdigest()
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM admin WHERE email_admin = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Cet email est déjà utilisé. Veuillez en utiliser un autre.", "danger")
                return redirect('/creer_compte_admin')

            try:
                cursor.execute("""INSERT INTO admin (nom_complet, email_admin, sexe, numero_telephone, password) 
                                VALUES (%s, %s, %s, %s, %s)""",
                               (nom_complet, email, sexe, numero_telephone, hashed_password))
                mysql.connection.commit()
                # 🔹 Envoi de l'email de confirmation (HTML bien design)
                msg = Message("Confirmation d'inscription", recipients=[email])
                msg.html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Bienvenue {prenom} !</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            text-align: center;
                            padding: 40px;
                        }}
                        .container {{
                            background: white;
                            padding: 20px;
                            max-width: 500px;
                            margin: auto;
                            border-radius: 10px;
                            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                        }}
                        h2 {{
                            color: #4CAF50;
                        }}
                        .info {{
                            text-align: left;
                            font-size: 16px;
                            margin: 20px 0;
                        }}
                        .info p {{
                            margin: 5px 0;
                        }}
                        .btn {{
                            display: inline-block;
                            padding: 10px 20px;
                            margin-top: 20px;
                            background: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            font-weight: bold;
                        }}
                        .footer {{
                            margin-top: 20px;
                            font-size: 12px;
                            color: #777;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Bienvenue, {prenom} ! 🎉</h2>
                        <p>Votre compte a été créé avec succès.</p>

                        <div class="info">
                            <p><strong>Nom :</strong> {nom_complet}</p>
                            <p><strong>Email :</strong> {email}</p>
                            <p><strong>Mot de passe :</strong> {password}</p>
                        </div>

                        <a class="btn" href="https://www.ab-naturel.com/">Se connecter</a>

                        <p class="footer">Si vous n'êtes pas à l'origine de cette inscription, ignorez cet email.</p>
                    </div>
                </body>
                </html>
                """

                mail.send(msg)
                flash("Compte créé avec succès. Un email de confirmation a été envoyé.", "success")
                return redirect('/login')

            except Exception as e:
                return f"Erreur lors de l'inscription : {e}"

        return render_template('admin/connexion/inscription.html', loggedIn=loggedIn, firstName=firstName,
                               userEmail=userEmail)
    else:
        return redirect(url_for('login'))