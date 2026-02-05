# Gestion des documents

Ce système permet aux administrateurs d'uploader des documents et d'insérer des liens vers ces documents dans les articles.

## Fonctionnalités

### Upload de documents
- Téléchargement de fichiers PDF, DOC, DOCX, XLS, XLSX, TXT
- Stockage dans `backend/src/main/resources/documents/`
- Validation automatique du format

### Liste des documents
- Affichage de tous les documents disponibles
- Nom du fichier et taille affichés
- Actions disponibles : Insérer, Voir, Supprimer

### Insertion dans les articles
- Bouton "Insérer" pour ajouter un lien dans l'éditeur
- Lien généré automatiquement au format HTML
- Ouverture dans un nouvel onglet

## Architecture

### Backend (Spring Boot)

#### DocumentController.java
- `POST /api/documents/upload` : Upload d'un document
- `GET /api/documents` : Liste tous les documents
- `GET /api/documents/{filename}` : Télécharge un document
- `DELETE /api/documents/{filename}` : Supprime un document

**Sécurité :**
- Upload/Liste/Suppression : Authentification requise (JWT)
- Téléchargement : Accès public (pour les visiteurs du site)

**Validation :**
- Nom de fichier sanitisé (caractères spéciaux supprimés)
- Types MIME corrects selon l'extension

### Frontend (Nuxt/Vue)

#### Page admin/actualites.vue

**Section "Gestion des documents" :**
1. **Upload** : Input file + bouton d'envoi
2. **Liste** : Tableau avec nom, taille, actions
3. **Bouton d'insertion** : Au-dessus de l'éditeur de contenu

**Fonctions principales :**
- `loadDocuments()` : Charge la liste des documents
- `uploadDocument()` : Upload un fichier vers l'API
- `deleteDocument()` : Supprime un document
- `insertDocumentLink()` : Insère le lien HTML dans l'éditeur
- `formatFileSize()` : Formate la taille du fichier

## Utilisation

### 1. Uploader un document

1. Aller dans "Admin > Actualités"
2. Section "Gestion des documents"
3. Cliquer sur "Choisir un fichier"
4. Sélectionner un fichier (PDF, DOC, etc.)
5. Cliquer sur "Envoyer"

### 2. Insérer un lien dans un article

**Méthode 1 : Depuis la liste des documents**
1. Rédiger votre article
2. Dans la section "Gestion des documents"
3. Cliquer sur "Insérer" à côté du document souhaité
4. Le lien est automatiquement ajouté au contenu

**Méthode 2 : Manuellement**
1. Copier l'URL du document : `http://localhost:8080/api/documents/nom-fichier.pdf`
2. Dans l'éditeur, créer un lien HTML :
   ```html
   <a href="/api/documents/nom-fichier.pdf" target="_blank">
     Télécharger le document
   </a>
   ```

### 3. Voir un document

- Cliquer sur "Voir" dans la liste des documents
- Ou accéder directement via l'URL : `/api/documents/{filename}`

### 4. Supprimer un document

1. Cliquer sur "Supprimer" à côté du document
2. Confirmer la suppression
3. Le fichier est supprimé du serveur

## Exemples de liens

### Lien simple
```html
<a href="/api/documents/rapport-2024.pdf" target="_blank">Rapport 2024</a>
```

### Lien avec icône
```html
<a href="/api/documents/presentation.pdf" target="_blank">
  📄 Télécharger la présentation (PDF)
</a>
```

### Lien stylisé
```html
<a href="/api/documents/formulaire.docx" target="_blank" 
   class="btn btn-primary">
  Télécharger le formulaire
</a>
```

## Configuration

### Emplacement des documents

**En développement local (sans Docker) :**
Les documents sont stockés dans :
```
backend/src/main/resources/documents/
```

**Avec Docker :**
Les documents sont stockés dans `/app/documents` à l'intérieur du conteneur, mais ce dossier est monté (volume) vers `./backend/src/main/resources/documents/` sur la machine hôte. Cela permet de :
- Voir les fichiers directement dans l'explorateur Windows
- Conserver les fichiers même si le conteneur est recréé
- Accéder aux fichiers depuis la machine hôte

Le volume est configuré dans `docker-compose.yml` :
```yaml
volumes:
  - ./backend/src/main/resources/documents:/app/documents
```

**Variable d'environnement :**
Vous pouvez personnaliser le chemin dans le conteneur en définissant `DOCUMENTS_DIR` dans `docker-compose.yml` (par défaut : `/app/documents`).

### Formats acceptés

- **PDF** : `.pdf`
- **Word** : `.doc`, `.docx`
- **Excel** : `.xls`, `.xlsx`
- **Texte** : `.txt`

### Taille maximale

Par défaut, Spring Boot limite la taille des fichiers. Pour modifier :

**application.properties**
```properties
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

## Sécurité

### Sanitisation des noms de fichiers
Les caractères spéciaux sont remplacés par des underscores :
- `mon fichier (2024).pdf` → `mon_fichier__2024_.pdf`

### Protection contre l'écrasement
Les fichiers avec le même nom sont automatiquement écrasés.
Pour éviter cela, renommer le fichier avant l'upload.

### Accès aux documents
- **Upload/Suppression** : Réservé aux administrateurs connectés
- **Consultation** : Public (accessible à tous les visiteurs)

## Maintenance

### Nettoyer les documents non utilisés

1. Lister tous les documents :
   ```bash
   ls backend/src/main/resources/documents/
   ```

2. Vérifier les liens dans les articles (base de données)

3. Supprimer les documents obsolètes via l'interface admin

### Sauvegarde

Les documents ne sont pas versionnés dans Git (`.gitignore`).

**Sauvegarde manuelle :**
```bash
# Copier le dossier documents
cp -r backend/src/main/resources/documents/ backup/documents-$(date +%Y%m%d)/
```

**Sauvegarde avec Docker :**
Avec le volume monté, les fichiers sont directement accessibles sur la machine hôte :
```bash
# Les fichiers sont déjà dans backend/src/main/resources/documents/
cp -r backend/src/main/resources/documents/ backup/documents-$(date +%Y%m%d)/
```

Si le volume n'est pas monté, vous pouvez copier depuis le conteneur :
```bash
docker cp gfz-backend:/app/documents ./backup/documents-$(date +%Y%m%d)/
```

## Dépannage

### Le document ne s'affiche pas
- Vérifier que le fichier existe dans `documents/`
- Vérifier l'URL dans l'article
- Vérifier les logs du backend

### Erreur lors de l'upload
- Vérifier la taille du fichier (< 10 MB par défaut)
- Vérifier le format du fichier
- Vérifier les permissions du dossier `documents/`
- Vérifier le token JWT (session admin)

### Erreur 404 sur un document
- Le fichier a peut-être été supprimé
- Vérifier l'orthographe du nom de fichier
- Les noms de fichiers sont sensibles à la casse

### Documents non visibles sur la machine hôte (Docker)
- Vérifier que le volume est bien monté dans `docker-compose.yml`
- Vérifier les logs du backend au démarrage : le chemin du dossier documents est affiché
- Vérifier que le dossier `backend/src/main/resources/documents/` existe sur la machine hôte
- Si les fichiers ne sont pas visibles, vérifier dans le conteneur :
  ```bash
  docker exec gfz-backend ls -la /app/documents
  ```
- Redémarrer les conteneurs après modification de `docker-compose.yml` :
  ```bash
  docker-compose down
  docker-compose up -d
  ```

## Évolutions possibles

- Gestion des versions de documents
- Dossiers/catégories pour organiser les documents
- Prévisualisation des documents PDF
- Compression automatique des fichiers
- Upload par glisser-déposer
- Barre de progression d'upload
- Métadonnées (date d'ajout, auteur, description)
