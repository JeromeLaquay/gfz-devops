#!/usr/bin/env python3
"""
Script pour extraire le contenu depuis une liste de liens d'articles
Utilisez ce script si vous avez déjà la liste complète des liens
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time

BASE_URL = "https://gfz-online.fr"

def nettoyer_texte(texte):
    """Nettoie le texte HTML et supprime les espaces superflus"""
    if not texte:
        return ""
    texte = re.sub(r'<[^>]+>', '', str(texte))
    texte = ' '.join(texte.split())
    return texte.strip()

def extraire_actualite_complete(url):
    """Extrait toutes les informations d'une page d'article complète"""
    actualite = {
        "titre": "",
        "contenu": "",
        "image": None,
        "dateCreation": None
    }
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraction du titre (chercher dans l'article spécifiquement)
        import re as re_module
        article_elem = soup.find('article', class_=re_module.compile('item'))
        if article_elem:
            page_header = article_elem.find('div', class_='page-header')
            if page_header:
                titre_elem = page_header.find('h1')
            else:
                titre_elem = article_elem.find('h1')
        else:
            component = soup.find('div', id='sp-component')
            if component:
                titre_elem = component.find('h1')
            else:
                # Chercher tous les h1 et ignorer celui du header
                tous_h1 = soup.find_all('h1')
                for h1 in tous_h1:
                    if not h1.find_parent('div', id='sp-logo') and not h1.find_parent('header'):
                        titre_elem = h1
                        break
        
        if titre_elem:
            span_format = titre_elem.find('span', class_='post-format')
            if span_format:
                span_format.decompose()
            titre_texte = nettoyer_texte(titre_elem.get_text())
            # Vérifier que ce n'est pas le titre du site
            if titre_texte and titre_texte != "Groupe Français des Zéolithes" and len(titre_texte) > 5:
                actualite["titre"] = titre_texte
            else:
                # Utiliser le title de la page
                title_tag = soup.find('title')
                if title_tag:
                    titre_complet = title_tag.get_text()
                    if ' - ' in titre_complet:
                        titre_extrait = titre_complet.split(' - ')[0].strip()
                        if titre_extrait and titre_extrait != "Groupe Français des Zéolithes":
                            actualite["titre"] = titre_extrait
        
        # Extraction du contenu HTML
        contenu_elem = soup.find('div', {'itemprop': 'articleBody'})
        if contenu_elem:
            for script in contenu_elem(["script", "style"]):
                script.decompose()
            actualite["contenu"] = str(contenu_elem)
        
        # Extraction de l'image
        img_elem = soup.find('div', class_='entry-image')
        if img_elem:
            img = img_elem.find('img', src=True)
            if img:
                actualite["image"] = urljoin(BASE_URL, img['src'])
        elif contenu_elem:
            img = contenu_elem.find('img', src=True)
            if img:
                actualite["image"] = urljoin(BASE_URL, img['src'])
        
        # Extraction de la date
        date_elem = soup.find(['time', 'span'], {'itemprop': 'datePublished'})
        if not date_elem:
            date_elem = soup.find('meta', {'property': 'article:published_time'})
            if date_elem:
                actualite["dateCreation"] = date_elem.get('content', '')
        
        if date_elem and not actualite["dateCreation"]:
            date_text = date_elem.get('datetime') or date_elem.get_text()
            actualite["dateCreation"] = nettoyer_texte(date_text)
        
    except Exception as e:
        print(f"  ⚠️  Erreur: {e}")
    
    return actualite

def sauvegarder_json(actualites, filename="actualites_export.json"):
    """Sauvegarde les actualités en JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(actualites, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {len(actualites)} actualités sauvegardées dans {filename}")

def generer_sql(actualites, filename="actualites_import.sql"):
    """Génère un script SQL pour importer les actualités"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("-- Import des actualités\n")
        f.write("-- Généré automatiquement\n\n")
        
        for act in actualites:
            titre = act["titre"].replace("'", "''")
            contenu = act["contenu"].replace("'", "''").replace("\\", "\\\\")
            image = act["image"].replace("'", "''") if act["image"] else None
            date = act["dateCreation"] or None
            
            f.write("INSERT INTO articles (titre, contenu, image, date_creation) VALUES\n")
            f.write(f"  ('{titre}', ")
            f.write(f"'{contenu}', ")
            if image:
                f.write(f"'{image}', ")
            else:
                f.write("NULL, ")
            if date:
                f.write(f"'{date}');\n\n")
            else:
                f.write("CURRENT_TIMESTAMP);\n\n")
    
    print(f"✅ Script SQL généré dans {filename}")

if __name__ == "__main__":
    # Liste des liens fournie par l'utilisateur
    liens = [
        "https://gfz-online.fr/fr/actualites/112-conference-internationale-materiaux-2026",
        "https://gfz-online.fr/fr/actualites/110-reunion-gfz-2026",
        "https://gfz-online.fr/fr/actualites/105-offre-de-these",
        "https://gfz-online.fr/fr/actualites/109-communication-de-surface-measurement-systems",
        "https://gfz-online.fr/fr/actualites/104-puits-de-science-12-avec-ludovic-pinard-tout-savoir-sur-les-zeolithes",
        "https://gfz-online.fr/fr/actualites/103-call-for-contributions-porousens-current-trends-and-future-directions-on-porous-composites-for-sensing-devices",
        "https://gfz-online.fr/fr/actualites/95-2023-french-german-adsorption-conference",
        "https://gfz-online.fr/fr/actualites/94-mecareact-paris-france-june-18-23-2023",
        "https://gfz-online.fr/fr/actualites/93-congres-isiem-2023"
    ]
    
    print("🚀 Extraction du contenu depuis les liens fournis...\n")
    print(f"📋 {len(liens)} liens à traiter\n")
    
    toutes_actualites = []
    
    for i, lien in enumerate(liens, 1):
        print(f"[{i}/{len(liens)}] Extraction de: {lien.split('/')[-1][:60]}...")
        actualite = extraire_actualite_complete(lien)
        if actualite["titre"]:
            toutes_actualites.append(actualite)
            print(f"  ✅ Titre: {actualite['titre'][:50]}...")
        else:
            print(f"  ⚠️  Titre manquant")
        time.sleep(0.5)
    
    if toutes_actualites:
        sauvegarder_json(toutes_actualites)
        generer_sql(toutes_actualites)
        print(f"\n✨ Terminé! {len(toutes_actualites)} actualités extraites.")
    else:
        print("\n❌ Aucune actualité extraite.")
