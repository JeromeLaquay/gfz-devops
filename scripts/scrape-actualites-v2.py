#!/usr/bin/env python3
"""
Script amélioré pour extraire toutes les actualités du site GFZ actuel
Version 2 : Extraction depuis toutes les pages avec meilleure détection
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time

BASE_URL = "https://gfz-online.fr"
ACTUALITES_URL = f"{BASE_URL}/fr/actualites"

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
        article_elem = soup.find('article', class_=re.compile('item'))
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

def extraire_tous_liens_page(url):
    """Extrait TOUS les liens d'articles depuis une page"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tous_liens = set()
        
        # Chercher TOUS les liens vers /fr/actualites/ID dans toute la page
        liens_elem = soup.find_all('a', href=re.compile(r'/fr/actualites/\d+'))
        
        for lien_elem in liens_elem:
            href = lien_elem.get('href', '')
            if href:
                lien = urljoin(BASE_URL, href)
                # Filtrer : doit être un lien d'article (pas la liste, pas la pagination)
                if (re.search(r'/fr/actualites/\d+', lien) and 
                    not re.search(r'/fr/actualites/?$', lien) and
                    '?start=' not in lien and 
                    '?page=' not in lien):
                    tous_liens.add(lien)
        
        return tous_liens
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return set()

def scraper_toutes_pages(nb_pages=9):
    """Scrape toutes les pages d'actualités"""
    print("\n🔍 Étape 1 : Extraction de tous les liens d'articles...\n")
    
    tous_liens = set()
    
    # Scraper chaque page
    for page in range(1, nb_pages + 1):
        print(f"📄 Page {page}/{nb_pages}")
        
        if page == 1:
            url = ACTUALITES_URL
        else:
            start = (page - 1) * 5  # CORRIGÉ : 5 articles par page (pas 20)
            url = f"{ACTUALITES_URL}?start={start}"
        
        print(f"  URL: {url}")
        liens = extraire_tous_liens_page(url)
        
        if liens:
            avant = len(tous_liens)
            tous_liens.update(liens)
            nouveaux = len(tous_liens) - avant
            print(f"  ✅ {nouveaux} nouveaux liens (Total: {len(tous_liens)})")
        else:
            print(f"  ⚠️  Aucun lien trouvé")
        
        time.sleep(1)
    
    print(f"\n✅ Total de {len(tous_liens)} liens uniques trouvés\n")
    
    if not tous_liens:
        print("❌ Aucun lien trouvé. Vérifiez la structure du site.")
        return []
    
    # Étape 2 : Extraire le contenu
    print("🔍 Étape 2 : Extraction du contenu de chaque article...\n")
    toutes_actualites = []
    
    liens_liste = sorted(list(tous_liens))
    for i, lien in enumerate(liens_liste, 1):
        print(f"  [{i}/{len(liens_liste)}] {lien.split('/')[-1][:60]}...")
        actualite = extraire_actualite_complete(lien)
        if actualite["titre"]:
            toutes_actualites.append(actualite)
        time.sleep(0.5)
    
    return toutes_actualites

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
    print("🚀 Début du scraping des actualités GFZ Online (v2)...\n")
    print(f"📍 URL: {BASE_URL}")
    print(f"📄 Pages à scraper: 9\n")
    
    reponse = input("Voulez-vous continuer? (o/n): ")
    if reponse.lower() != 'o':
        print("Annulé.")
        exit()
    
    print("\n" + "="*60)
    print("DÉBUT DU SCRAPING")
    print("="*60 + "\n")
    
    actualites = scraper_toutes_pages(9)
    
    print("\n" + "="*60)
    print("FIN DU SCRAPING")
    print("="*60 + "\n")
    
    if actualites:
        sauvegarder_json(actualites)
        generer_sql(actualites)
        print(f"\n✨ Terminé! {len(actualites)} actualités extraites.")
    else:
        print("\n❌ Aucune actualité trouvée.")
