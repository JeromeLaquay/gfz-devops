# Guide de scraping des actualités

## Méthode 1 : Script Python automatisé (Recommandé)

### Prérequis
```bash
pip install requests beautifulsoup4
```

### Utilisation
1. Modifiez les URLs dans `scrape-actualites.py` :
   - `BASE_URL` : URL de base du site actuel
   - `ACTUALITES_URL` : URL de la page des actualités

2. Ajustez les sélecteurs CSS si nécessaire (selon la structure HTML réelle)

3. Exécutez :
```bash
python scripts/scrape-actualites.py
```

4. Le script génère :
   - `actualites_export.json` : Données au format JSON
   - `actualites_import.sql` : Script SQL pour import direct

---

## Méthode 2 : Extension navigateur (Plus simple, manuel)

### Avec l'extension "Web Scraper" (Chrome/Edge)

1. Installez l'extension "Web Scraper" depuis le Chrome Web Store

2. Ouvrez la page des actualités

3. Créez un nouveau sitemap :
   - Nom : "GFZ Actualités"
   - Start URL : URL de la première page des actualités

4. Configurez les sélecteurs :
   - **Article** : Sélecteur pour chaque article (ex: `.article`, `article`, etc.)
   - **Titre** : Sélecteur pour le titre (ex: `h2`, `.title`)
   - **Contenu** : Sélecteur pour le texte (ex: `.content`, `p`)
   - **Image** : Sélecteur pour l'image (ex: `img`)
   - **Lien** : Sélecteur pour le lien complet

5. Configurez la pagination :
   - Type : "Link"
   - Sélecteur : Le lien "Suivant" ou les numéros de page

6. Lancez le scraping et exportez en CSV/JSON

---

## Méthode 3 : Outil en ligne (Rapide)

### Utiliser "Import.io" ou "ParseHub"

1. Allez sur https://www.parsehub.com/ ou https://www.import.io/

2. Créez un nouveau projet

3. Entrez l'URL de la première page des actualités

4. Sélectionnez les éléments à extraire (titre, contenu, image)

5. Configurez la pagination automatique

6. Lancez et exportez les données

---

## Méthode 4 : Copie manuelle structurée (Si les autres échouent)

### Avec Excel/Google Sheets

1. Créez un fichier avec les colonnes :
   - Titre
   - Contenu
   - Image (URL)
   - Date

2. Pour chaque page (1 à 9) :
   - Copiez les titres dans la colonne Titre
   - Copiez les contenus dans la colonne Contenu
   - Copiez les URLs des images dans la colonne Image
   - Ajoutez les dates si disponibles

3. Exportez en CSV

4. Utilisez un script de conversion CSV vers SQL

---

## Import dans la nouvelle base de données

### Option A : Via l'interface admin
1. Connectez-vous à l'interface admin
2. Allez dans "Actualités"
3. Créez chaque article manuellement ou importez via l'API

### Option B : Via SQL direct
1. Utilisez le fichier `actualites_import.sql` généré
2. Exécutez-le dans votre base de données PostgreSQL :
```bash
psql -U gfzuser -d gfzdb -f actualites_import.sql
```

### Option C : Via script d'import
Créez un script qui lit le JSON et utilise l'API pour créer les articles.

---

## Conseils

- **Testez d'abord sur 1-2 pages** avant de scraper toutes les 9 pages
- **Vérifiez les sélecteurs CSS** - ils peuvent varier selon la structure HTML
- **Respectez le robots.txt** et ne surchargez pas le serveur (pauses entre requêtes)
- **Sauvegardez régulièrement** pendant le scraping
- **Vérifiez les données** avant l'import final

---

## Dépannage

### Le script ne trouve pas les articles
- Inspectez le HTML de la page (F12)
- Ajustez les sélecteurs CSS dans le script
- Vérifiez que le contenu n'est pas chargé dynamiquement (JavaScript)

### Les images ne s'affichent pas
- Vérifiez que les URLs sont absolues ou convertissez-les
- Téléchargez les images localement si nécessaire

### Le contenu est incomplet
- Le script essaie d'extraire le contenu complet depuis la page de l'article
- Vérifiez que les liens sont corrects
