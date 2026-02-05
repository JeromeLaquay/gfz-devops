# Installation de Python pour Windows

## Option 1 : Installer Python depuis python.org (Recommandé)

1. **Télécharger Python** :
   - Allez sur https://www.python.org/downloads/
   - Téléchargez la dernière version (Python 3.12 ou 3.11)

2. **Installer Python** :
   - Exécutez le fichier téléchargé
   - ⚠️ **IMPORTANT** : Cochez "Add Python to PATH" lors de l'installation
   - Cliquez sur "Install Now"

3. **Vérifier l'installation** :
   - Ouvrez un nouveau terminal (PowerShell ou CMD)
   - Tapez : `python --version`
   - Vous devriez voir la version de Python

4. **Installer les dépendances** :
   ```bash
   python -m pip install requests beautifulsoup4
   ```

5. **Lancer le script** :
   ```bash
   cd scripts
   python scrape-actualites.py
   ```

---

## Option 2 : Utiliser py launcher (si Python est déjà installé)

Si Python est installé mais pas dans le PATH, essayez :

```bash
py scrape-actualites.py
```

Ou avec la version spécifique :
```bash
py -3 scrape-actualites.py
```

---

## Option 3 : Alternative sans Python - Extension navigateur

Si vous ne voulez pas installer Python, utilisez l'extension **Web Scraper** :

1. **Installer l'extension** :
   - Chrome : https://chrome.google.com/webstore/detail/web-scraper/jnhgnonknehpejjnehehllkliplmbmhn
   - Edge : Recherchez "Web Scraper" dans le Microsoft Edge Add-ons

2. **Ouvrir la page des actualités** :
   - Allez sur https://gfz-online.fr/fr/actualites

3. **Créer un sitemap** :
   - Ouvrez l'extension Web Scraper (icône dans la barre d'outils)
   - Cliquez sur "Create new sitemap" > "Create sitemap"
   - Nom : "GFZ Actualités"
   - Start URL : `https://gfz-online.fr/fr/actualites`

4. **Configurer les sélecteurs** :
   - Cliquez sur "Add new selector"
   - **Type** : Element
   - **ID** : `article`
   - **Sélecteur** : `article.item` (ou inspectez la page pour trouver le bon sélecteur)
   - **Multiple** : Oui
   - Cliquez sur "Save selector"

   - Ajoutez des sélecteurs enfants :
     - **Titre** : `h1` ou `.page-header h1`
     - **Lien** : `a` (attribut href)
     - **Image** : `img` (attribut src)

5. **Configurer la pagination** :
   - Ajoutez un sélecteur de type "Link"
   - **ID** : `next_page`
   - **Sélecteur** : Le lien "Suivant" ou les numéros de page
   - **Multiple** : Oui

6. **Lancer le scraping** :
   - Cliquez sur "Scrape"
   - L'extension va visiter toutes les pages automatiquement

7. **Exporter les données** :
   - Une fois terminé, cliquez sur "Export data"
   - Choisissez CSV ou JSON
   - Les données seront téléchargées

---

## Option 4 : Utiliser PowerShell avec Python intégré

Si vous avez Windows 11 avec Python pré-installé :

```powershell
python3 scrape-actualites.py
```

Ou :

```powershell
py -3 scrape-actualites.py
```

---

## Vérification rapide

Pour vérifier si Python est installé, essayez ces commandes dans l'ordre :

```bash
python --version
python3 --version
py --version
py -3 --version
```

Si aucune ne fonctionne, Python n'est pas installé ou pas dans le PATH.

---

## Solution rapide : Installer Python via Microsoft Store

1. Ouvrez le Microsoft Store
2. Recherchez "Python 3.12" ou "Python 3.11"
3. Cliquez sur "Installer"
4. Une fois installé, redémarrez le terminal
5. Essayez `python scrape-actualites.py`
