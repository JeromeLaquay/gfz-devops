# Gestion des doublons dans la table articles

Ce fichier contient des requêtes SQL pour identifier et gérer les titres en doublon dans la table `articles`.

## Fichier

- `trouver-doublons.sql` : Requêtes SQL pour trouver et gérer les doublons

## Requêtes disponibles

### 1. Liste simple des titres en doublon
Affiche les titres qui apparaissent plusieurs fois avec leur nombre d'occurrences.

```sql
SELECT titre, COUNT(*) as nombre_occurrences
FROM articles
GROUP BY titre
HAVING COUNT(*) > 1
ORDER BY nombre_occurrences DESC, titre;
```

**Résultat :**
| titre | nombre_occurrences |
|-------|-------------------|
| Article X | 3 |
| Article Y | 2 |

---

### 2. Détails complets des articles en doublon
Liste tous les articles ayant un titre en doublon avec leurs détails.

**Colonnes affichées :**
- `id` : Identifiant de l'article
- `titre` : Titre de l'article
- `date_creation` : Date de création
- `longueur_contenu` : Nombre de caractères du contenu
- `longueur_image` : Nombre de caractères de l'image

---

### 3. Comparaison des doublons
Groupe les doublons ensemble pour faciliter la comparaison.

**Colonnes affichées :**
- `titre` : Titre de l'article
- `nb_occurrences` : Nombre de doublons
- `ids` : Liste des IDs séparés par des virgules
- `dates` : Liste des dates de création

---

### 4. Identifier les doublons à supprimer (garder le plus récent)
Liste les articles à supprimer en conservant la version la plus récente.

---

### 5. Identifier les doublons à supprimer (garder le plus ancien)
Liste les articles à supprimer en conservant la version la plus ancienne.

---

### 6. Statistiques sur les doublons
Affiche un résumé :
- Nombre de titres uniques
- Nombre total d'articles
- Nombre de doublons

---

### 7. Supprimer les doublons (garde le plus récent)
⚠️ **ATTENTION : Requête de suppression réelle**

Supprime tous les doublons en gardant l'article le plus récent pour chaque titre.

**À décommenter pour exécuter.**

---

### 8. Supprimer les doublons (garde le plus ancien)
⚠️ **ATTENTION : Requête de suppression réelle**

Supprime tous les doublons en gardant l'article le plus ancien pour chaque titre.

**À décommenter pour exécuter.**

---

### 9. Trouver les doublons exacts
Identifie les articles ayant exactement le même titre ET le même contenu.

Utilise un hash MD5 du contenu pour la comparaison.

---

### 10. Trouver les doublons partiels
Identifie les articles avec le même titre mais un contenu différent.

Permet de distinguer :
- **Doublon exact** : Même titre + même contenu
- **Contenu différent** : Même titre mais contenu différent

---

## Utilisation

### Avec psql (PostgreSQL)

```bash
# Se connecter à la base de données
psql -U postgres -d gfz_online

# Exécuter le fichier
\i scripts/trouver-doublons.sql

# Ou exécuter une requête spécifique
\i scripts/trouver-doublons.sql
```

### Avec pgAdmin ou DBeaver

1. Ouvrir le fichier `trouver-doublons.sql`
2. Copier la requête souhaitée
3. Coller dans l'éditeur SQL
4. Exécuter

### Avec Docker Compose

```bash
# Se connecter au conteneur PostgreSQL
docker-compose exec db psql -U postgres -d gfz_online

# Puis exécuter les requêtes
```

## Stratégie de nettoyage recommandée

### Étape 1 : Identifier
```sql
-- Vérifier combien de doublons existent
SELECT titre, COUNT(*) as nb
FROM articles
GROUP BY titre
HAVING COUNT(*) > 1;
```

### Étape 2 : Analyser
```sql
-- Examiner les détails des doublons
SELECT id, titre, date_creation, LENGTH(contenu)
FROM articles
WHERE titre IN (
    SELECT titre FROM articles 
    GROUP BY titre HAVING COUNT(*) > 1
)
ORDER BY titre, date_creation;
```

### Étape 3 : Décider
Choisir la stratégie :
- **Garder le plus récent** : Si les mises à jour sont importantes
- **Garder le plus ancien** : Si la date de publication originale compte
- **Examen manuel** : Si les contenus sont différents

### Étape 4 : Sauvegarder
```bash
# Créer une sauvegarde avant suppression
pg_dump -U postgres gfz_online > backup_avant_nettoyage.sql
```

### Étape 5 : Supprimer
Décommenter et exécuter la requête appropriée (7 ou 8).

### Étape 6 : Vérifier
```sql
-- Vérifier qu'il n'y a plus de doublons
SELECT COUNT(*) - COUNT(DISTINCT titre) as doublons_restants
FROM articles;
```

## Exemple de workflow complet

```sql
-- 1. Statistiques initiales
SELECT 
    COUNT(DISTINCT titre) as titres_uniques,
    COUNT(*) as total_articles,
    COUNT(*) - COUNT(DISTINCT titre) as doublons
FROM articles;

-- 2. Liste des doublons
SELECT titre, COUNT(*) as nb
FROM articles
GROUP BY titre
HAVING COUNT(*) > 1;

-- 3. Examiner un doublon spécifique
SELECT id, titre, date_creation, 
       LEFT(contenu, 100) as apercu_contenu
FROM articles
WHERE titre = 'Titre du doublon'
ORDER BY date_creation;

-- 4. Créer une sauvegarde
-- (via pg_dump ou export)

-- 5. Supprimer (garder le plus récent)
DELETE FROM articles a
WHERE a.id NOT IN (
    SELECT MAX(id)
    FROM articles
    GROUP BY titre
);

-- 6. Vérification finale
SELECT COUNT(*) - COUNT(DISTINCT titre) as doublons_restants
FROM articles;
```

## Notes importantes

- **Toujours faire une sauvegarde** avant d'exécuter des requêtes de suppression
- Les requêtes de suppression (7 et 8) sont commentées par défaut
- Pour les doublons avec contenu différent, un examen manuel est recommandé
- Le hash MD5 permet de comparer rapidement des contenus longs

## En cas de problème

Si vous supprimez accidentellement des articles :

```bash
# Restaurer depuis la sauvegarde
psql -U postgres -d gfz_online < backup_avant_nettoyage.sql
```
