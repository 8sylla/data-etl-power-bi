# Convention de Nommage - Projet BI École

## 1. TABLES
- Dimensions : `dim_[nom]` (ex: dim_etudiant, dim_filiere)
- Faits : `fait_[nom]` (ex: fait_absences, fait_notes)
- Tout en minuscules avec underscore

## 2. COLONNES
- Format : `nom_colonne` (ex: student_id, full_name, date_naissance)
- Clés primaires : `[table]_id` (ex: student_id, filiere_id)
- Clés étrangères : même nom que la clé primaire référencée
- Dates : préfixe `date_` (ex: date_examen, date_cours)
- Booléens : préfixe `is_` (ex: is_active, is_partner)

## 3. MESURES DAX
- Format : `[Nom Complet]` avec majuscules (ex: [Taux Absence], [Moyenne Générale])
- Mesures intermédiaires : préfixe `_` (ex: [_Total Heures])

## 4. FICHIERS
- Scripts : `xx_nom_script.py` (ex: 01_nettoyage_csv.py)
- Documentation : `xx_nom_doc.md`
- Exports : `export_nom_YYYYMMDD.csv`