# Guide rapide - Gestion des documents

## Uploader un document

1. Aller dans **Admin > Actualités**
2. Section "Gestion des documents"
3. Choisir un fichier (PDF, DOC, XLS, etc.)
4. Cliquer sur "Envoyer"

## Insérer un lien dans un article

### Option 1 : Automatique
1. Rédiger votre article
2. Cliquer sur "Insérer" à côté du document
3. Le lien est ajouté au contenu

### Option 2 : Manuel
Bouton "📎 Insérer un lien vers un document" au-dessus de l'éditeur

## Format du lien généré

```html
<a href="/api/documents/nom-fichier.pdf" target="_blank">nom-fichier.pdf</a>
```

## Personnaliser le texte du lien

Après insertion, modifiez le texte entre les balises `<a>` :

```html
<!-- Avant -->
<a href="/api/documents/rapport.pdf" target="_blank">rapport.pdf</a>

<!-- Après -->
<a href="/api/documents/rapport.pdf" target="_blank">📄 Télécharger le rapport annuel</a>
```

## Supprimer un document

1. Dans la liste des documents
2. Cliquer sur "Supprimer"
3. Confirmer

⚠️ **Attention** : Les liens dans les articles existants seront cassés !

## Formats acceptés

✅ PDF, DOC, DOCX, XLS, XLSX, TXT

## Taille maximale

📦 10 MB par fichier (configurable)

## Exemples de liens stylisés

```html
<!-- Avec icône -->
<a href="/api/documents/guide.pdf" target="_blank">
  📄 Guide d'utilisation (PDF)
</a>

<!-- Avec bouton -->
<p>
  <a href="/api/documents/formulaire.docx" 
     target="_blank" 
     style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
    Télécharger le formulaire
  </a>
</p>

<!-- Liste de documents -->
<ul>
  <li><a href="/api/documents/doc1.pdf" target="_blank">Document 1</a></li>
  <li><a href="/api/documents/doc2.pdf" target="_blank">Document 2</a></li>
  <li><a href="/api/documents/doc3.pdf" target="_blank">Document 3</a></li>
</ul>
```

## Astuce

Pour organiser vos documents, utilisez des préfixes dans les noms de fichiers :

- `2024_rapport_annuel.pdf`
- `2024_budget_previsionnel.xlsx`
- `guide_utilisateur_v2.pdf`
- `formulaire_adhesion_2024.docx`

Cela facilite le tri et la recherche !
