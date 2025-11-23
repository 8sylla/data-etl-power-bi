import pandas as pd
import numpy as np
from datetime import datetime
import os

# Configuration
INPUT_DIR = "../01_donnees/data_raw"
OUTPUT_DIR = "../01_donnees/data_clean"
ENCODING = "utf-8-sig"  # UTF-8 avec BOM pour Power BI

# Créer le dossier de sortie
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def snake_case(text):
    """Convertir CamelCase en snake_case"""
    import re
    text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
    return text.lower()

def clean_column_names(df):
    """Standardiser les noms de colonnes"""
    df.columns = [snake_case(col) for col in df.columns]
    return df

def convert_date(date_str, input_format="%Y-%m-%d"):
    """Convertir dates au format ISO (YYYY-MM-DD)"""
    try:
        if pd.isna(date_str):
            return None
        return pd.to_datetime(date_str, format=input_format).strftime("%Y-%m-%d")
    except:
        return None

def convert_date2(date_str, input_format="%d-%m-%Y"):
    """Convertir dates au format ISO (YYYY-MM-DD)"""
    try:
        if pd.isna(date_str):
            return None
        return pd.to_datetime(date_str, format=input_format).strftime("%Y-%m-%d")
    except:
        return None
    
def normalize_date(date_str, intval=8, year_sigmoid=2000):
    """
    date_str est du type 'yyyy-mm-dd', par ex : '0007-16-03'
    On projette l'année entre 2000 et 2000 + intval - 1 (par défaut 2000–2007)
    et on renvoie au format 'yyyy-mm-dd'.
    """
    year, month, day = date_str.split("-")
    year_int = int(year)
    new_year = year_sigmoid + (year_int % intval)   # force entre 2000 et 2007
    return f"{new_year:04d}-{month}-{day}"

def normalize_date2(date_str, intval=8, year_sigmoid=2000):
    """
    date_str est du type 'dd-mm-yyyy', par ex : '16-03-0007'
    On projette l'année entre 2000 et 2000 + intval - 1 (par défaut 2000–2007)
    et on renvoie au format 'yyyy-mm-dd'.
    """
    day, month, year = date_str.split("-")  # dd, mm, yyyy

    year_int = int(year)            # on utilise bien l'année
    new_year = year_sigmoid + (year_int % intval)  # force entre 2000 

    # on reformate proprement en yyyy-mm-dd
    return f"{new_year:04d}-{int(month):02d}-{int(day):02d}"

def replace_columns_value_with_int_valuer(data_val, start, end, randomize=False):
    if randomize:
        import random
        return random.randint(start, end)
    return start + (data_val % end)
    

# ========================================
# 1. DIM_ETUDIANT
# ========================================
print("📌 Nettoyage: dim_etudiant...")
df_student = pd.read_csv(f"{INPUT_DIR}/studentDim.csv", sep=";", encoding=ENCODING)
df_student = clean_column_names(df_student)

# Renommer colonnes spécifiques
df_student.rename(columns={
    'date_of_birth': 'date_naissance',
    'enrollment_year': 'annee_inscription',
}, inplace=True)

# Convertir dates
df_student['date_naissance'] = df_student['date_naissance'].apply(
    lambda x: normalize_date(x)
)

# Normaliser le genre
df_student['gender'] = df_student['gender'].str.upper().str.strip().map({'M': 'M', 'F': 'F', 'MALE': 'M', 'FEMALE': 'F'})

# Sauvegarder
df_student.to_csv(f"{OUTPUT_DIR}/dim_etudiant.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_student)} lignes exportées")

# ========================================
# 2. DIM_FILIERE
# ========================================
print("\n📌 Nettoyage: dim_filiere...")
df_filiere = pd.read_csv(f"{INPUT_DIR}/filiereDim.csv", sep=";", encoding=ENCODING)
df_filiere = clean_column_names(df_filiere)



df_filiere.rename(columns={
    'filiere_name': 'filiere_code',
    'full_name': 'filiere_nom',
    'date_creation':'date_creation'
}, inplace=True)

df_filiere['date_creation'] = df_filiere['date_creation'].apply(convert_date)
df_filiere.to_csv(f"{OUTPUT_DIR}/dim_filiere.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_filiere)} lignes exportées")

# ========================================
# 3. DIM_GROUPE
# ========================================
print("\n📌 Nettoyage: dim_groupe...")
df_group = pd.read_csv(f"{INPUT_DIR}/groupDim.csv", sep=";", encoding=ENCODING)
df_group = clean_column_names(df_group)

df_group.rename(columns={
    'groupid': 'group_id',
    'group_name': 'group_nom',
    'academic_year': 'annee_academique',
    'filiereid': 'filiere_id'
}, inplace=True)

df_group.to_csv(f"{OUTPUT_DIR}/dim_groupe.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_group)} lignes exportées")

# ========================================
# 4. DIM_MATIERE
# ========================================
print("\n📌 Nettoyage: dim_matiere...")
df_matiere = pd.read_csv(f"{INPUT_DIR}/MatiereDim.csv", sep=";", encoding=ENCODING)
df_matiere = clean_column_names(df_matiere)

# Les colonnes semblent désordonnées, reconstruction
df_matiere.columns = ['matiere_id', 'matiere_nom', 'matiere_code', 'col_vide', 
                      'niveau', 'credits', 'type_cours', 'date_creation']

df_matiere = df_matiere[['matiere_id', 'matiere_nom', 'matiere_code', 'niveau', 
                         'credits', 'type_cours', 'date_creation']]

df_matiere['date_creation'] = df_matiere['date_creation'].apply(convert_date)
df_matiere.to_csv(f"{OUTPUT_DIR}/dim_matiere.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_matiere)} lignes exportées")

# ========================================
# 5. DIM_SEMESTRE
# ========================================
print("\n📌 Nettoyage: dim_semestre...")
df_semestre = pd.read_csv(f"{INPUT_DIR}/semestreDim.csv", sep=";", encoding=ENCODING)
df_semestre = clean_column_names(df_semestre)

df_semestre.rename(columns={
    'semester_id': 'semestre_id',
    'academic_year': 'annee_academique',
    'semestre_name': 'semestre_nom',
    'start_date': 'date_debut',
    'end_date': 'date_fin',
    'is_active': 'is_active',
    'date_creation': 'date_creation'
}, inplace=True)

df_semestre['date_debut'] = df_semestre['date_debut'].apply(convert_date)
df_semestre['date_fin'] = df_semestre['date_fin'].apply(convert_date)
df_semestre['date_creation'] = df_semestre['date_creation'].apply(convert_date)
df_semestre['is_active'] = df_semestre['is_active'].astype(int)

df_semestre.to_csv(f"{OUTPUT_DIR}/dim_semestre.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_semestre)} lignes exportées")

# ========================================
# 6. DIM_ENSEIGNANT
# ========================================
print("\n📌 Nettoyage: dim_enseignant...")
df_enseignant = pd.read_csv(f"{INPUT_DIR}/EnseignantDim.csv", sep=";", encoding=ENCODING)
df_enseignant = clean_column_names(df_enseignant)

df_enseignant.rename(columns={
    'enseignantid': 'enseignant_id',
    'fullname': 'full_name',
    'hire_date': 'date_embauche'
}, inplace=True)

df_enseignant['date_embauche'] = df_enseignant['date_embauche'].apply(convert_date)
df_enseignant['status'] = df_enseignant['status'].str.capitalize()
df_enseignant['qualification'] = df_enseignant['qualification'].str.capitalize()

df_enseignant.to_csv(f"{OUTPUT_DIR}/dim_enseignant.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_enseignant)} lignes exportées")

# ========================================
# 7. DIM_ENTREPRISE
# ========================================
print("\n📌 Nettoyage: dim_entreprise...")
df_entreprise = pd.read_csv(f"{INPUT_DIR}/entrepriseDim.csv", sep=";", encoding=ENCODING)
df_entreprise = clean_column_names(df_entreprise)

df_entreprise.rename(columns={
    'entrepriseid': 'entreprise_id',
    'entreprise_name': 'entreprise_nom',
    'contact_person': 'contact_personne',
    'datecreation': 'date_creation'
}, inplace=True)

df_entreprise['date_creation'] = df_entreprise['date_creation'].apply(convert_date)
df_entreprise['is_partner'] = df_entreprise['is_partner'].astype(int)

df_entreprise.to_csv(f"{OUTPUT_DIR}/dim_entreprise.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_entreprise)} lignes exportées")

# ========================================
# 8. FAIT_ABSENCES
# ========================================
print("\n📌 Nettoyage: fait_absences...")
df_absences = pd.read_csv(f"{INPUT_DIR}/FAIT_Absences.csv", sep=";", encoding=ENCODING)

# Colonnes attendues
df_absences.columns = ['absence_id', 'student_id', 'matiere_id', 'semaine', 
                       'mois', 'date_absence', 'type_absence', 'is_justifiee', 
                       'heures_manquees', 'date_saisie']

df_absences['date_absence'] = df_absences['date_absence'].apply(
    lambda x: normalize_date2(x,2,2023)
)
df_absences['date_saisie'] = df_absences['date_saisie'].apply(
    lambda x: convert_date(x, "%d-%m-%Y") if pd.notna(x) else None
)

df_absences.to_csv(f"{OUTPUT_DIR}/fait_absences.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_absences)} lignes exportées")

# ========================================
# 9. FAIT_NOTES
# ========================================
print("\n📌 Nettoyage: fait_notes...")
df_notes = pd.read_csv(f"{INPUT_DIR}/FAIT_notes.csv", sep=";", encoding=ENCODING)
df_notes = clean_column_names(df_notes)

df_notes.rename(columns={
    'noteid': 'note_id',
    'studentid': 'student_id',
    'matiereid': 'matiere_id',
    'semestreid': 'semestre_id',
    'typeevaluation': 'type_evaluation',
    'dateexamen': 'date_examen',
    'groupid': 'group_id',
    'noteponderee': 'note_ponderee'
}, inplace=True)

df_notes['date_examen'] = df_notes['date_examen'].apply(lambda x: normalize_date2(x, 2, 2023))
df_notes['semestre_id'] = df_notes['semestre_id'].apply(lambda x: replace_columns_value_with_int_valuer(1,1,4, randomize=True))
df_notes['group_id'] = df_notes['group_id'].apply(lambda x: replace_columns_value_with_int_valuer(x,1,30))
df_notes.to_csv(f"{OUTPUT_DIR}/fait_notes.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_notes)} lignes exportées")

# ========================================
# 10. FAIT_STAGES
# ========================================
print("\n📌 Nettoyage: fait_stages...")
df_stage = pd.read_csv(f"{INPUT_DIR}/fait_stage.csv", sep=";", encoding=ENCODING)
df_stage = clean_column_names(df_stage)

df_stage.rename(columns={
    'stageid': 'stage_id',
    'studentid': 'student_id',
    'entrepriseid': 'entreprise_id',
    'typestage': 'type_stage',
    'filiere_id': 'filiere_id',
    'semestreid': 'semestre_id',
    'start_date': 'date_debut',
    'end_date': 'date_fin',
    'supervisor_name': 'encadrant_nom'
}, inplace=True)

df_stage['date_debut'] = df_stage['date_debut'].apply(lambda x: normalize_date2(x,3,2023))
df_stage['date_fin'] = df_stage['date_fin'].apply(lambda x: normalize_date2(x,3,2023))

df_stage.to_csv(f"{OUTPUT_DIR}/fait_stages.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_stage)} lignes exportées")

# ========================================
# 11. FAIT_HEURES_ENSEIGNEMENT
# ========================================
print("\n📌 Nettoyage: fait_heures_enseignement...")
df_heures = pd.read_csv(f"{INPUT_DIR}/fait_heures_enseignement.csv", sep=";", encoding=ENCODING)
df_heures = clean_column_names(df_heures)

df_heures.rename(columns={
    'heureid': 'heure_id',
    'enseignantid': 'enseignant_id',
    'matiereid': 'matiere_id',
    'groupid': 'group_id',
    'semestreid': 'semestre_id',
    'typecours': 'type_cours',
    'volumehoraire': 'volume_horaire',
    'datecours': 'date_cours'
}, inplace=True)

df_heures['date_cours'] = df_heures['date_cours'].apply(lambda x: normalize_date2(x,2,2023))
df_heures['group_id'] = df_heures['group_id'].apply(lambda x: replace_columns_value_with_int_valuer(x,1,30))
df_heures['semestre_id'] = df_heures['semestre_id'].apply(lambda x: replace_columns_value_with_int_valuer(1,1,4, randomize=True))
df_heures.to_csv(f"{OUTPUT_DIR}/fait_heures_enseignement.csv", index=False, encoding=ENCODING)
print(f"✅ {len(df_heures)} lignes exportées")

print("\n" + "="*60)
print("✅ NETTOYAGE TERMINÉ - Tous les fichiers dans 'data_clean/'")
print("="*60)

