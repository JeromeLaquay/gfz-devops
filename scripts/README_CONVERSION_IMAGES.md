# Conversion des images en base64

Ce script convertit toutes les images référencées dans le fichier SQL en data URIs (base64).

## Utilisation

### Prérequis

```bash
pip install requests
```

### Exécution

```bash
python convertir-images-base64.py
```

Ou avec des fichiers personnalisés :

```bash
python convertir-images-base64.py fichier_entree.sql fichier_sortie.sql
```

## Fonctionnalités

- ✅ Détecte automatiquement toutes les URLs d'images dans le fichier SQL
- ✅ Télécharge chaque image depuis le serveur
- ✅ Convertit en base64 avec détection automatique du type MIME
- ✅ Remplace les URLs dans :
  - La colonne `image` des INSERT
  - Les balises `<img>` dans le contenu HTML
  - Les autres attributs contenant des URLs d'images
- ✅ Gère les URLs absolues et relatives
- ✅ Génère un fichier SQL modifié avec les data URIs

## Types d'images supportés

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## Format de sortie

Les images sont converties en data URIs au format :
```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
```

## Notes

- Le script fait une pause de 0.5 secondes entre chaque téléchargement pour éviter de surcharger le serveur
- Les images qui ne peuvent pas être téléchargées sont ignorées (l'URL originale est conservée)
- Le fichier de sortie est sauvegardé avec l'encodage UTF-8

## Exemple de sortie

```
🖼️  Conversion des images en base64

📖 Lecture de actualites_import.sql...
🔍 Extraction des URLs d'images...
📋 34 images trouvées

[1/34] https://gfz-online.fr/images/actus/Capture_decran_2025-06-27_a_135619.png
  📥 Téléchargement: https://gfz-online.fr/images/actus/Capture_decran_2025-06-27_a_135619.png
  ✅ Converti en image/png (123456 bytes)
...

✅ 34/34 images converties avec succès

🔄 Remplacement des URLs par les data URIs...
💾 Sauvegarde dans actualites_import_base64.sql...

✅ Conversion terminée !
📊 Statistiques:
   - Images trouvées: 34
   - Images converties: 34
   - Échecs: 0
```
