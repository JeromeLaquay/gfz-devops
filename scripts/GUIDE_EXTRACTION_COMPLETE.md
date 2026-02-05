# Guide pour extraire TOUTES les actualités (9 pages × 5 articles = 45 articles)

## Problème identifié

La pagination Joomla utilise un **incrément de 5** (pas 20) :
- Page 1 : `https://gfz-online.fr/fr/actualites`
- Page 2 : `https://gfz-online.fr/fr/actualites?start=5`
- Page 3 : `https://gfz-online.fr/fr/actualites?start=10`
- ...
- Page 9 : `https://gfz-online.fr/fr/actualites?start=40`

## Solution 1 : Script JavaScript dans le navigateur (RECOMMANDÉ)

### Étape 1 : Ouvrir la console
1. Allez sur https://gfz-online.fr/fr/actualites
2. Appuyez sur F12 pour ouvrir les outils développeur
3. Allez dans l'onglet "Console"

### Étape 2 : Copier-coller le script
Copiez le contenu de `extraire-tous-liens.js` et collez-le dans la console, puis appuyez sur Entrée.

Le script va :
- Visiter automatiquement les 9 pages
- Extraire tous les liens d'articles
- Afficher le résultat dans la console
- Copier automatiquement dans le presse-papiers

### Étape 3 : Sauvegarder les liens
1. Le résultat JSON sera dans la console
2. Copiez-le et sauvegardez-le dans un fichier `liens_complets.json`

### Étape 4 : Extraire le contenu
Utilisez le script Python `extraire-depuis-liens.py` en modifiant la liste des liens dedans.

---

## Solution 2 : Script Python corrigé

Le script `scrape-actualites-v2.py` a été corrigé pour utiliser l'incrément de 5.

```bash
python scrape-actualites-v2.py
```

---

## Solution 3 : Script manuel page par page

Si les scripts automatiques ne fonctionnent pas, vous pouvez extraire manuellement :

### Pour chaque page (1 à 9) :

1. Ouvrez la page dans votre navigateur
2. Ouvrez la console (F12)
3. Collez ce code :

```javascript
const liens = [];
document.querySelectorAll('a[href*="/fr/actualites/"]').forEach(a => {
    const href = a.href;
    if (href.match(/\/fr\/actualites\/\d+/) && 
        !href.includes('?start=') && 
        !href.includes('?page=') &&
        !href.endsWith('/fr/actualites')) {
        if (!liens.includes(href)) {
            liens.push(href);
        }
    }
});
console.log(JSON.stringify(liens, null, 2));
copy(JSON.stringify(liens, null, 2));
```

4. Copiez les liens affichés
5. Répétez pour chaque page
6. Combine tous les liens dans un seul fichier JSON

---

## Solution 4 : Utiliser le script avec liste de liens

Si vous avez déjà extrait tous les liens (comme les 9 que vous avez fournis), modifiez `extraire-depuis-liens.py` :

1. Ouvrez `extraire-depuis-liens.py`
2. Remplacez la liste `liens = [...]` par votre liste complète
3. Exécutez : `python extraire-depuis-liens.py`

---

## Format attendu

Vous devriez avoir environ **45 liens** (9 pages × 5 articles).

Format d'un lien : `https://gfz-online.fr/fr/actualites/ID-titre-de-l-article`

---

## Après extraction

Une fois tous les liens extraits, le script générera :
- `actualites_export.json` : Toutes les données
- `actualites_import.sql` : Script SQL pour import direct
