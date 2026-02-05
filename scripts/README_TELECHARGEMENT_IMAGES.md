# Téléchargement des images depuis le fichier SQL

Ce script permet de télécharger les images référencées dans le fichier `actualites_import.sql` et de les enregistrer dans le dossier `images` avec le titre de l'article correspondant.

## Prérequis

- Python 3.7 ou supérieur
- Connexion Internet

## Utilisation

### Méthode 1 : Via le fichier batch (Windows)

Double-cliquez sur le fichier :
```
lancer-telechargement-images.bat
```

### Méthode 2 : Via la ligne de commande

```bash
cd scripts
python telecharger-images.py
```

## Fonctionnement

Le script :
1. Lit le fichier `actualites_import.sql`
2. Extrait tous les titres d'articles et leurs URLs d'images
3. Télécharge chaque image depuis `https://gfz-online.fr/images/actus/...`
4. Nomme le fichier avec le titre de l'article (nettoyé)
5. Enregistre les images dans le dossier `scripts/images/`

## Format des noms de fichiers

Les titres sont nettoyés pour créer des noms de fichiers valides :
- Suppression des caractères spéciaux (`< > : " / \ | ? *`)
- Remplacement des espaces par des underscores (`_`)
- Limitation à 100 caractères
- Conservation de l'extension originale (`.jpg`, `.png`, etc.)

### Exemples

| Titre de l'article | Nom du fichier |
|-------------------|----------------|
| "Prix de thèse du GFZ" | `Prix_de_these_du_GFZ.png` |
| "Réunion GFZ 2017" | `Reunion_GFZ_2017.jpg` |

## Structure des fichiers

```
scripts/
├── actualites_import.sql          # Fichier SQL source
├── telecharger-images.py          # Script Python
├── lancer-telechargement-images.bat  # Lanceur Windows
├── README_TELECHARGEMENT_IMAGES.md   # Cette documentation
└── images/                        # Dossier de destination
    ├── Prix_de_these_du_GFZ.png
    ├── Reunion_GFZ_2017.jpg
    └── ...
```

## Gestion des erreurs

Le script gère automatiquement :
- Images déjà téléchargées (pas de re-téléchargement)
- Erreurs HTTP (404, 403, etc.)
- Erreurs de connexion
- Timeout (10 secondes)

Un résumé est affiché à la fin avec :
- Nombre de téléchargements réussis
- Nombre d'échecs
- Total d'articles traités

## Exemple de sortie

```
Lecture du fichier actualites_import.sql...
Trouvé 10 articles avec images

Dossier de destination: C:\...\scripts\images

[1/10] Call for Contributions - POROUSens: Current Trends and...
  URL: https://gfz-online.fr/images/actus/Capture_decran_2025-06-27_a_135619.png
  Fichier: Call_for_Contributions_-_POROUSens_Current_Trends_and.png
  Téléchargé avec succès

[2/10] Prix de thèse du GFZ...
  URL: https://gfz-online.fr/images/actus/Actu03_2017_PrixThese.png
  Fichier: Prix_de_these_du_GFZ.png
  Téléchargé avec succès

...

============================================================
Résumé:
  Réussis: 8
  Échecs: 2
  Total: 10
============================================================
```

## Remarques

- Les images sont téléchargées uniquement si elles n'existent pas déjà
- Le script utilise un User-Agent pour éviter d'être bloqué
- Les timeouts sont configurés à 10 secondes par image
