USE medijutsu;

INSERT INTO hconsultation(
id , etat ,patient_id ,doctor_id ,motif)
values( 1 , "malade" , 1 , 1 , "crise_cardiaque");

INSERT INTO produits (reference , nom_produit , quantite , date_expiration)
values("ref" ,"claire",1,12-12-2024),
      ("code","ameyo",2,31-12-2000);
DROP TABLES produits ;

INSERT INTO produits (reference , nom_produit , quantite)
values("ref" ,"claire",1),
      ("code","ameyo",2);




      
      
      


