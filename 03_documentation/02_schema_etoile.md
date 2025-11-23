# Schéma en Étoile - DataWarehouse École d'Ingénieurs

## 🌟 ARCHITECTURE GÉNÉRALE
```
                    dim_semestre
                         |
                         |
    dim_enseignant ----  |  ---- dim_matiere
            |            |            |
            |            |            |
    fait_heures_enseignement    fait_absences
                              fait_notes
                         |    fait_stages
                         |         |
    dim_groupe ------    |    -----+---- dim_entreprise
         |               |              
         |               |
    dim_filiere ---- dim_etudiant
```

## 📊 TABLES DE DIMENSIONS

### 1. dim_etudiant
- **Clé primaire :** student_id
- **Attributs :** full_name, gender, date_naissance, level, cycle, annee_inscription, status
- **Clés étrangères :** filiere_id, group_id

### 2. dim_filiere
- **Clé primaire :** filiere_id
- **Attributs :** filiere_code, filiere_nom, date_creation

### 3. dim_groupe
- **Clé primaire :** group_id
- **Attributs :** group_nom, level, annee_academique
- **Clés étrangères :** filiere_id

### 4. dim_matiere
- **Clé primaire :** matiere_id
- **Attributs :** matiere_nom, matiere_code, niveau, credits, type_cours, date_creation

### 5. dim_semestre
- **Clé primaire :** semestre_id
- **Attributs :** annee_academique, semestre_nom, date_debut, date_fin, is_active, date_creation

### 6. dim_enseignant
- **Clé primaire :** enseignant_id
- **Attributs :** full_name, status, qualification, department, date_embauche, email

### 7. dim_entreprise
- **Clé primaire :** entreprise_id
- **Attributs :** entreprise_nom, sector, city, region, country, contact_personne, email, phone, is_partner, date_creation

## 📈 TABLES DE FAITS

### 1. fait_absences
- **Granularité :** Une ligne par absence
- **Clés étrangères :** student_id, matiere_id
- **Métriques :** heures_manquees, is_justifiee
- **Dimensions temporelles :** date_absence, semaine, mois

### 2. fait_notes
- **Granularité :** Une ligne par évaluation
- **Clés étrangères :** student_id, matiere_id, semestre_id, group_id
- **Métriques :** note, coefficient, note_ponderee
- **Dimensions temporelles :** date_examen

### 3. fait_stages
- **Granularité :** Une ligne par stage
- **Clés étrangères :** student_id, entreprise_id, filiere_id, semestre_id
- **Métriques :** grade
- **Dimensions temporelles :** date_debut, date_fin
- **Attributs :** type_stage, encadrant_nom, status

### 4. fait_heures_enseignement
- **Granularité :** Une ligne par séance de cours
- **Clés étrangères :** enseignant_id, matiere_id, group_id, semestre_id
- **Métriques :** volume_horaire
- **Dimensions temporelles :** date_cours
- **Attributs :** type_cours

## 🔗 RELATIONS

| Table Enfant | Colonne FK | Table Parent | Cardinalité |
|--------------|-----------|--------------|-------------|
| dim_etudiant | filiere_id | dim_filiere | N:1 |
| dim_etudiant | group_id | dim_groupe | N:1 |
| dim_groupe | filiere_id | dim_filiere | N:1 |
| fait_absences | student_id | dim_etudiant | N:1 |
| fait_absences | matiere_id | dim_matiere | N:1 |
| fait_notes | student_id | dim_etudiant | N:1 |
| fait_notes | matiere_id | dim_matiere | N:1 |
| fait_notes | semestre_id | dim_semestre | N:1 |
| fait_notes | group_id | dim_groupe | N:1 |
| fait_stages | student_id | dim_etudiant | N:1 |
| fait_stages | entreprise_id | dim_entreprise | N:1 |
| fait_stages | filiere_id | dim_filiere | N:1 |
| fait_stages | semestre_id | dim_semestre | N:1 |
| fait_heures_enseignement | enseignant_id | dim_enseignant | N:1 |
| fait_heures_enseignement | matiere_id | dim_matiere | N:1 |
| fait_heures_enseignement | group_id | dim_groupe | N:1 |
| fait_heures_enseignement | semestre_id | dim_semestre | N:1 |
```

