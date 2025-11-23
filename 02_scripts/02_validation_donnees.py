import pandas as pd
import os

CLEAN_DIR = "../01_donnees/data_clean"

def validate_csv(filename, expected_cols, key_col):
    """Valider un fichier CSV"""
    filepath = f"{CLEAN_DIR}/{filename}"
    
    if not os.path.exists(filepath):
        print(f"❌ {filename} - FICHIER MANQUANT")
        return False
    
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    
    # Vérifier colonnes
    missing_cols = set(expected_cols) - set(df.columns)
    if missing_cols:
        print(f"❌ {filename} - Colonnes manquantes: {missing_cols}")
        return False
    
    # Vérifier clé primaire
    if df[key_col].isna().any():
        print(f"⚠️  {filename} - Valeurs NULL dans {key_col}")
    
    if df[key_col].duplicated().any():
        print(f"❌ {filename} - Doublons dans {key_col}")
        return False
    
    print(f"✅ {filename} - OK ({len(df)} lignes)")
    return True

# Validation des dimensions
print("🔍 VALIDATION DES DIMENSIONS\n")

validate_csv("dim_etudiant.csv", 
            ['student_id', 'full_name', 'gender', 'date_naissance', 'level', 
             'cycle', 'annee_inscription', 'status', 'filiere_id', 'group_id'],
            'student_id')

validate_csv("dim_filiere.csv",
            ['filiere_id', 'filiere_code', 'filiere_nom', 'date_creation'],
            'filiere_id')

validate_csv("dim_groupe.csv",
            ['group_id', 'group_nom', 'level', 'annee_academique', 'filiere_id'],
            'group_id')

validate_csv("dim_matiere.csv",
            ['matiere_id', 'matiere_nom', 'matiere_code', 'niveau', 'credits', 
             'type_cours', 'date_creation'],
            'matiere_id')

validate_csv("dim_semestre.csv",
            ['semestre_id', 'annee_academique', 'semestre_nom', 'date_debut', 
             'date_fin', 'is_active', 'date_creation'],
            'semestre_id')

validate_csv("dim_enseignant.csv",
            ['enseignant_id', 'full_name', 'status', 'qualification', 
             'department', 'date_embauche', 'email'],
            'enseignant_id')

validate_csv("dim_entreprise.csv",
            ['entreprise_id', 'entreprise_nom', 'sector', 'city', 'region', 
             'country', 'contact_personne', 'email', 'phone', 'is_partner', 
             'date_creation'],
            'entreprise_id')

# Validation des faits
print("\n🔍 VALIDATION DES TABLES DE FAITS\n")

validate_csv("fait_absences.csv",
            ['absence_id', 'student_id', 'matiere_id', 'semaine', 'mois', 
             'date_absence', 'type_absence', 'is_justifiee', 'heures_manquees', 
             'date_saisie'],
            'absence_id')

validate_csv("fait_notes.csv",
            ['note_id', 'student_id', 'matiere_id', 'semestre_id', 
             'type_evaluation', 'note', 'coefficient', 'date_examen', 
             'group_id', 'note_ponderee'],
            'note_id')

validate_csv("fait_stages.csv",
            ['stage_id', 'student_id', 'entreprise_id', 'type_stage', 
             'filiere_id', 'semestre_id', 'date_debut', 'date_fin', 
             'encadrant_nom', 'grade', 'status'],
            'stage_id')

validate_csv("fait_heures_enseignement.csv",
            ['heure_id', 'enseignant_id', 'matiere_id', 'group_id', 
             'semestre_id', 'type_cours', 'volume_horaire', 'date_cours'],
            'heure_id')

print("\n" + "="*60)
print("✅ VALIDATION TERMINÉE")
print("="*60)