-- ============================================
-- Requêtes pour trouver les doublons
-- ============================================

-- 1. LISTE SIMPLE DES TITRES EN DOUBLON
-- Affiche uniquement les titres qui apparaissent plusieurs fois
SELECT 
    titre, 
    COUNT(*) as nombre_occurrences
FROM articles
GROUP BY titre
HAVING COUNT(*) > 1
ORDER BY nombre_occurrences DESC, titre;


-- 2. DÉTAILS COMPLETS DES ARTICLES EN DOUBLON
-- Affiche tous les détails des articles ayant un titre en doublon
SELECT 
    a.id,
    a.titre,
    a.date_creation,
    LENGTH(a.contenu) as longueur_contenu,
    LENGTH(a.image) as longueur_image
FROM articles a
WHERE a.titre IN (
    SELECT titre
    FROM articles
    GROUP BY titre
    HAVING COUNT(*) > 1
)
ORDER BY a.titre, a.date_creation;


-- 3. COMPARAISON DES DOUBLONS
-- Compare les doublons côte à côte avec leur contenu
SELECT 
    a.titre,
    COUNT(*) as nb_occurrences,
    STRING_AGG(a.id::text, ', ') as ids,
    STRING_AGG(
        TO_CHAR(a.date_creation, 'YYYY-MM-DD HH24:MI'), 
        ' | '
    ) as dates
FROM articles a
WHERE a.titre IN (
    SELECT titre
    FROM articles
    GROUP BY titre
    HAVING COUNT(*) > 1
)
GROUP BY a.titre
ORDER BY nb_occurrences DESC, a.titre;


-- 4. GARDER LE PLUS RÉCENT, SUPPRIMER LES AUTRES
-- Identifie les doublons à supprimer (garde le plus récent)
SELECT 
    a.id,
    a.titre,
    a.date_creation,
    'À SUPPRIMER' as action
FROM articles a
WHERE EXISTS (
    SELECT 1
    FROM articles a2
    WHERE a2.titre = a.titre
    AND a2.date_creation > a.date_creation
)
ORDER BY a.titre, a.date_creation;


-- 5. GARDER LE PLUS ANCIEN, SUPPRIMER LES AUTRES
-- Identifie les doublons à supprimer (garde le plus ancien)
SELECT 
    a.id,
    a.titre,
    a.date_creation,
    'À SUPPRIMER' as action
FROM articles a
WHERE EXISTS (
    SELECT 1
    FROM articles a2
    WHERE a2.titre = a.titre
    AND a2.date_creation < a.date_creation
)
ORDER BY a.titre, a.date_creation;


-- 6. COMPTER TOUS LES DOUBLONS
-- Statistiques sur les doublons
SELECT 
    COUNT(DISTINCT titre) as titres_uniques,
    COUNT(*) as total_articles,
    COUNT(*) - COUNT(DISTINCT titre) as nombre_doublons
FROM articles;


-- 7. SUPPRIMER LES DOUBLONS (GARDE LE PLUS RÉCENT)
-- ⚠️ ATTENTION : Cette requête SUPPRIME réellement les doublons
-- Décommenter pour exécuter
/*
DELETE FROM articles a
WHERE a.id NOT IN (
    SELECT MAX(id)
    FROM articles
    GROUP BY titre
);
*/


-- 8. SUPPRIMER LES DOUBLONS (GARDE LE PLUS ANCIEN)
-- ⚠️ ATTENTION : Cette requête SUPPRIME réellement les doublons
-- Décommenter pour exécuter
/*
DELETE FROM articles a
WHERE a.id NOT IN (
    SELECT MIN(id)
    FROM articles
    GROUP BY titre
);
*/


-- 9. TROUVER LES DOUBLONS EXACTS (même titre ET même contenu)
-- Utile pour identifier les vrais doublons complets
SELECT 
    titre,
    MD5(contenu) as hash_contenu,
    COUNT(*) as nombre_occurrences,
    STRING_AGG(id::text, ', ') as ids
FROM articles
GROUP BY titre, MD5(contenu)
HAVING COUNT(*) > 1
ORDER BY nombre_occurrences DESC;


-- 10. TROUVER LES DOUBLONS PARTIELS (même titre, contenu différent)
-- Identifie les articles avec le même titre mais un contenu différent
WITH doublons_titre AS (
    SELECT titre
    FROM articles
    GROUP BY titre
    HAVING COUNT(*) > 1
)
SELECT 
    a.id,
    a.titre,
    a.date_creation,
    MD5(a.contenu) as hash_contenu,
    CASE 
        WHEN COUNT(*) OVER (PARTITION BY a.titre, MD5(a.contenu)) > 1 
        THEN 'Doublon exact'
        ELSE 'Contenu différent'
    END as type_doublon
FROM articles a
INNER JOIN doublons_titre d ON a.titre = d.titre
ORDER BY a.titre, a.date_creation;
