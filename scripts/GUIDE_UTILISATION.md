# Guide d'utilisation du script de scraping

## ⚠️ Python n'est pas installé ?

Si vous voyez "Python est introuvable", consultez **INSTALLATION_PYTHON.md** pour installer Python ou utilisez l'alternative avec l'extension Web Scraper (plus simple, pas besoin de Python).

---

## Installation des dépendances

Une fois Python installé :

```bash
pip install requests beautifulsoup4
```

Ou :
```bash
python -m pip install requests beautifulsoup4
```

## Lancement du script

### Méthode 1 : Script batch (Windows - le plus simple)

Double-cliquez sur `lancer-scraping.bat` dans le dossier scripts.

### Méthode 2 : Directement avec Python

```bash
cd scripts
python scrape-actualites.py
```

### Méthode 3 : Avec Python 3 explicitement

```bash
cd scripts
python3 scrape-actualites.py
```

### Méthode 4 : Avec py launcher (Windows)

```cmd
cd scripts
py scrape-actualites.py
```

## Ce que fait le script

1. **Scrape les 9 pages** de la liste des actualités
2. **Extrait les liens** vers chaque article
3. **Visite chaque article** pour extraire :
   - Le titre
   - Le contenu complet (en HTML)
   - L'image principale
   - La date de publication (si disponible)
4. **Génère 2 fichiers** :
   - `actualites_export.json` : Données au format JSON
   - `actualites_import.sql` : Script SQL pour import direct

## Durée estimée

- **Temps total** : 15-30 minutes selon le nombre d'articles
- Le script fait des pauses entre les requêtes pour ne pas surcharger le serveur

## Résultat

Après l'exécution, vous aurez :
- ✅ Toutes les actualités dans `actualites_export.json`
- ✅ Un script SQL prêt à importer dans `actualites_import.sql`

## Import dans la nouvelle base de données

### Option 1 : Via l'interface admin
1. Connectez-vous à `/admin`
2. Allez dans "Actualités"
3. Créez chaque article manuellement en copiant depuis le JSON

### Option 2 : Via script d'import API
```bash
python import-actualites-api.py actualites_export.json [VOTRE_TOKEN_JWT]
```

### Option 3 : Via SQL direct
```bash
psql -U gfzuser -d gfzdb -f actualites_import.sql
```

## Dépannage

### Erreur "Module not found"
```bash
pip install requests beautifulsoup4
```

### Aucune actualité trouvée
- Vérifiez votre connexion internet
- Vérifiez que le site https://gfz-online.fr est accessible
- Le script peut nécessiter des ajustements des sélecteurs CSS

### Le script est trop lent
- C'est normal, il fait des pauses pour respecter le serveur
- Vous pouvez réduire les pauses dans le code (mais attention à ne pas surcharger le serveur)
