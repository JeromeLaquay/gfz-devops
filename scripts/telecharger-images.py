import re
import os
import urllib.request
import urllib.error
from pathlib import Path

def nettoyer_nom_fichier(nom):
    """Nettoie le nom pour en faire un nom de fichier valide."""
    nom = re.sub(r'[<>:"/\\|?*]', '', nom)
    nom = nom.replace(' ', '_')
    nom = nom[:100]
    return nom

def extraire_articles(fichier_sql):
    """Extrait les titres et URLs d'images du fichier SQL."""
    print(f"Lecture du fichier {fichier_sql}...")
    
    with open(fichier_sql, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    pattern = r"INSERT INTO articles \(titre, contenu, image, date_creation\) VALUES\s*\('([^']+)',\s*'.*?',\s*'(https://gfz-online\.fr/images/actus/[^']+)'"
    
    matches = re.finditer(pattern, contenu, re.DOTALL)
    
    articles = []
    for match in matches:
        titre = match.group(1)
        url_image = match.group(2)
        articles.append({
            'titre': titre,
            'url': url_image
        })
    
    print(f"Trouvé {len(articles)} articles avec images")
    return articles

def telecharger_image(url, chemin_destination):
    """Télécharge une image depuis une URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        request = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(request, timeout=10) as response:
            with open(chemin_destination, 'wb') as f:
                f.write(response.read())
        
        return True
    except urllib.error.HTTPError as e:
        print(f"  Erreur HTTP {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"  Erreur URL: {e.reason}")
        return False
    except Exception as e:
        print(f"  Erreur: {str(e)}")
        return False

def telecharger_images(articles, dossier_images):
    """Télécharge toutes les images."""
    Path(dossier_images).mkdir(parents=True, exist_ok=True)
    
    print(f"\nDossier de destination: {dossier_images}\n")
    
    succes = 0
    echecs = 0
    
    for i, article in enumerate(articles, 1):
        titre = article['titre']
        url = article['url']
        
        extension = os.path.splitext(url)[1]
        nom_fichier = nettoyer_nom_fichier(titre) + extension
        chemin_complet = os.path.join(dossier_images, nom_fichier)
        
        print(f"[{i}/{len(articles)}] {titre[:60]}...")
        print(f"  URL: {url}")
        print(f"  Fichier: {nom_fichier}")
        
        if os.path.exists(chemin_complet):
            print(f"  Déjà téléchargé")
            succes += 1
        else:
            if telecharger_image(url, chemin_complet):
                print(f"  Téléchargé avec succès")
                succes += 1
            else:
                echecs += 1
        
        print()
    
    print(f"\n{'='*60}")
    print(f"Résumé:")
    print(f"  Réussis: {succes}")
    print(f"  Échecs: {echecs}")
    print(f"  Total: {len(articles)}")
    print(f"{'='*60}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fichier_sql = os.path.join(script_dir, 'actualites_import.sql')
    dossier_images = os.path.join(script_dir, 'images')
    
    if not os.path.exists(fichier_sql):
        print(f"Erreur: fichier {fichier_sql} introuvable")
        return
    
    articles = extraire_articles(fichier_sql)
    
    if not articles:
        print("Aucun article avec image trouvé")
        return
    
    telecharger_images(articles, dossier_images)

if __name__ == '__main__':
    main()
