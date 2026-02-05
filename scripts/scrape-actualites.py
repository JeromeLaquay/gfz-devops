#!/usr/bin/env python3
"""
Script pour extraire toutes les actualités du site GFZ actuel
et les formater pour importation dans la nouvelle base de données
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
import time

BASE_URL = "https://gfz-online.fr"
ACTUALITES_URL = f"{BASE_URL}/fr/actualites"

def nettoyer_texte(texte):
    """Nettoie le texte HTML et supprime les espaces superflus"""
    if not texte:
        return ""
    # Supprime les balises HTML
    texte = re.sub(r'<[^>]+>', '', str(texte))
    # Nettoie les espaces
    texte = ' '.join(texte.split())
    return texte.strip()

def extraire_lien_article(article_element, base_url):
    """Extrait le lien vers la page complète de l'article"""
    # Chercher le lien dans différents endroits
    lien_elem = article_element.find('a', href=True)
    if lien_elem and lien_elem.get('href'):
        lien = lien_elem['href']
        if lien.startswith('http'):
            return lien
        lien_complet = urljoin(base_url, lien)
        # Vérifier que c'est bien un lien d'article (contient un ID)
        if re.search(r'/fr/actualites/\d+', lien_complet):
            return lien_complet
    return None

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
        # Le titre est dans <article class="item item-page"> > <div class="page-header"> > <h1>
        article_elem = soup.find('article', class_=re.compile('item'))
        if article_elem:
            page_header = article_elem.find('div', class_='page-header')
            if page_header:
                titre_elem = page_header.find('h1')
            else:
                titre_elem = article_elem.find('h1')
        else:
            # Fallback : chercher dans sp-component
            component = soup.find('div', id='sp-component')
            if component:
                titre_elem = component.find('h1')
            else:
                # Dernier recours : chercher tous les h1 et prendre celui qui n'est pas dans le header
                tous_h1 = soup.find_all('h1')
                for h1 in tous_h1:
                    # Ignorer le h1 du header (dans sp-logo)
                    if not h1.find_parent('div', id='sp-logo') and not h1.find_parent('header'):
                        titre_elem = h1
                        break
        
        if titre_elem:
            # Enlever l'icône si présente
            span_format = titre_elem.find('span', class_='post-format')
            if span_format:
                span_format.decompose()
            titre_texte = nettoyer_texte(titre_elem.get_text())
            # Vérifier que ce n'est pas le titre du site
            if titre_texte and titre_texte != "Groupe Français des Zéolithes" and len(titre_texte) > 5:
                actualite["titre"] = titre_texte
            else:
                # Utiliser le title de la page (format: "Titre - Groupe Français des Zéolithes - GFZ")
                title_tag = soup.find('title')
                if title_tag:
                    titre_complet = title_tag.get_text()
                    # Format: "Titre - Groupe Français des Zéolithes - GFZ"
                    if ' - ' in titre_complet:
                        titre_extrait = titre_complet.split(' - ')[0].strip()
                        if titre_extrait and titre_extrait != "Groupe Français des Zéolithes":
                            actualite["titre"] = titre_extrait
        
        # Extraction du contenu (dans div avec itemprop="articleBody")
        contenu_elem = soup.find('div', {'itemprop': 'articleBody'})
        if contenu_elem:
            # Garder le HTML pour préserver la mise en forme
            # Supprimer les scripts et styles
            for script in contenu_elem(["script", "style"]):
                script.decompose()
            
            # Extraire le HTML propre
            contenu_html = str(contenu_elem)
            actualite["contenu"] = contenu_html
        
        # Extraction de l'image principale (dans div.entry-image ou dans le contenu)
        img_elem = soup.find('div', class_='entry-image')
        if img_elem:
            img = img_elem.find('img', src=True)
            if img:
                actualite["image"] = urljoin(BASE_URL, img['src'])
        else:
            # Chercher la première image dans le contenu
            img = contenu_elem.find('img', src=True) if contenu_elem else None
            if img:
                actualite["image"] = urljoin(BASE_URL, img['src'])
        
        # Extraction de la date (peut être dans les métadonnées)
        # Joomla peut stocker la date dans différentes balises
        date_elem = soup.find(['time', 'span'], {'itemprop': 'datePublished'})
        if not date_elem:
            date_elem = soup.find('meta', {'property': 'article:published_time'})
            if date_elem:
                actualite["dateCreation"] = date_elem.get('content', '')
        
        if date_elem and not actualite["dateCreation"]:
            date_text = date_elem.get('datetime') or date_elem.get_text()
            actualite["dateCreation"] = nettoyer_texte(date_text)
        
    except Exception as e:
        print(f"  ⚠️  Erreur lors de l'extraction de {url}: {e}")
    
    return actualite

def scraper_liste_actualites(numero_page):
    """Scrape la page de liste des actualités et extrait les liens"""
    # Format Joomla : /fr/actualites?start=X (20 articles par page généralement)
    # Ou /fr/actualites?page=X
    if numero_page == 1:
        url = ACTUALITES_URL
    else:
        start = (numero_page - 1) * 5  # Joomla utilise 5 articles par page pour ce site
        url = f"{ACTUALITES_URL}?start={start}"
    
    print(f"Scraping liste page {numero_page} ({url})...")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        liens_articles = []
        
        # Méthode 1 : Chercher TOUS les liens vers /fr/actualites/ID-... dans toute la page
        # Pattern plus large pour capturer tous les formats possibles
        tous_liens = soup.find_all('a', href=re.compile(r'/fr/actualites/\d+'))
        for lien_elem in tous_liens:
            href = lien_elem.get('href', '')
            if href:
                lien = urljoin(BASE_URL, href)
                # Filtrer : doit contenir un ID numérique suivi d'un tiret (format article)
                # ou juste un ID (format simple)
                if re.search(r'/fr/actualites/\d+', lien):
                    # Exclure les liens vers la page de liste elle-même
                    if not re.search(r'/fr/actualites/?$', lien) and lien not in liens_articles:
                        liens_articles.append(lien)
        
        # Méthode 2 : Chercher dans le contenu principal (sp-component)
        content_area = soup.find('div', id='sp-component')
        if content_area:
            liens_content = content_area.find_all('a', href=re.compile(r'/fr/actualites/\d+'))
            for lien_elem in liens_content:
                href = lien_elem.get('href', '')
                if href:
                    lien = urljoin(BASE_URL, href)
                    if re.search(r'/fr/actualites/\d+', lien) and not re.search(r'/fr/actualites/?$', lien):
                        if lien not in liens_articles:
                            liens_articles.append(lien)
        
        # Méthode 3 : Chercher dans les articles structurés
        articles = soup.find_all('article', class_=re.compile('item', re.I))
        if not articles:
            articles = soup.find_all('div', class_=re.compile('item|article|news', re.I))
        
        for article in articles:
            lien = extraire_lien_article(article, BASE_URL)
            if lien and lien not in liens_articles:
                liens_articles.append(lien)
        
        # Nettoyer les liens : enlever les doublons et les liens invalides
        liens_articles_clean = []
        for lien in liens_articles:
            # Vérifier que c'est bien un lien d'article (contient un ID)
            if re.search(r'/fr/actualites/\d+', lien):
                # Exclure les liens de pagination et la page de liste
                if '?start=' not in lien and '?page=' not in lien:
                    if lien not in liens_articles_clean:
                        liens_articles_clean.append(lien)
        
        # Debug : afficher quelques liens trouvés
        if liens_articles_clean:
            print(f"  → Exemples de liens trouvés:")
            for lien_ex in liens_articles_clean[:3]:
                print(f"     - {lien_ex[:80]}...")
        
        print(f"  → Total: {len(liens_articles_clean)} liens d'articles trouvés")
        return liens_articles_clean
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return []

def scraper_page(numero_page):
    """Scrape une page de liste et extrait les articles complets"""
    liens = scraper_liste_actualites(numero_page)
    
    if not liens:
        return []
    
    actualites = []
    for i, lien in enumerate(liens, 1):
        print(f"  [{i}/{len(liens)}] Extraction de: {lien.split('/')[-1][:50]}...")
        actualite = extraire_actualite_complete(lien)
        if actualite["titre"]:
            actualites.append(actualite)
        time.sleep(0.5)  # Pause entre chaque article
    
    return actualites

def extraire_tous_liens_depuis_page(url):
    """Extrait TOUS les liens d'articles depuis une page donnée"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tous_liens = set()
        
        # Chercher TOUS les liens vers /fr/actualites/ID dans toute la page
        tous_liens_elem = soup.find_all('a', href=re.compile(r'/fr/actualites/\d+'))
        for lien_elem in tous_liens_elem:
            href = lien_elem.get('href', '')
            if href:
                lien = urljoin(BASE_URL, href)
                # Exclure les liens vers la page de liste elle-même
                if re.search(r'/fr/actualites/\d+', lien) and not re.search(r'/fr/actualites/?$', lien):
                    # Exclure aussi les liens de pagination (qui pointent vers ?start=X)
                    if '?start=' not in lien and '?page=' not in lien:
                        tous_liens.add(lien)
        
        return tous_liens
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return set()

def scraper_toutes_pages(nb_pages=9):
    """Scrape toutes les pages d'actualités"""
    print("\n🔍 Étape 1 : Extraction de tous les liens d'articles...\n")
    
    # D'abord, collecter TOUS les liens depuis toutes les pages
    tous_liens = set()
    
    for page in range(1, nb_pages + 1):
        print(f"📄 Page {page}/{nb_pages}")
        liens = scraper_liste_actualites(page)
        
        # Si on trouve des liens, les ajouter
        if liens:
            tous_liens.update(liens)
            print(f"  ✅ {len(liens)} liens ajoutés (Total: {len(tous_liens)})")
        else:
            print(f"  ⚠️  Aucun lien trouvé avec la méthode normale")
            # Essayer une méthode alternative : extraire tous les liens de la page
            url_page = ACTUALITES_URL if page == 1 else f"{ACTUALITES_URL}?start={(page-1)*20}"
            liens_alternatifs = extraire_tous_liens_depuis_page(url_page)
            if liens_alternatifs:
                tous_liens.update(liens_alternatifs)
                print(f"  → {len(liens_alternatifs)} liens trouvés avec méthode alternative (Total: {len(tous_liens)})")
        
        time.sleep(1)  # Pause entre chaque page
    
    print(f"\n✅ Total de {len(tous_liens)} liens uniques trouvés\n")
    
    if not tous_liens:
        print("❌ Aucun lien trouvé.")
        print("💡 Suggestions:")
        print("   - Vérifiez que le site est accessible")
        print("   - Vérifiez le format de pagination (peut-être différent de ?start=X)")
        print("   - Essayez de visiter manuellement quelques pages pour voir le format")
        return []
    
    # Ensuite, extraire le contenu de chaque article
    print("🔍 Étape 2 : Extraction du contenu de chaque article...\n")
    toutes_actualites = []
    
    liens_liste = sorted(list(tous_liens))  # Trier pour avoir un ordre cohérent
    for i, lien in enumerate(liens_liste, 1):
        print(f"  [{i}/{len(liens_liste)}] Extraction de: {lien.split('/')[-1][:60]}...")
        actualite = extraire_actualite_complete(lien)
        if actualite["titre"]:
            toutes_actualites.append(actualite)
        else:
            print(f"     ⚠️  Titre manquant, article ignoré")
        time.sleep(0.5)  # Pause entre chaque article
    
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
        
        for i, act in enumerate(actualites, 1):
            titre = act["titre"].replace("'", "''")
            # Le contenu est en HTML, donc on doit échapper les quotes
            contenu = act["contenu"].replace("'", "''").replace("\\", "\\\\")
            image = act["image"].replace("'", "''") if act["image"] else None
            date = act["dateCreation"] or None
            
            f.write(f"INSERT INTO articles (titre, contenu, image, date_creation) VALUES\n")
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
    print("🚀 Début du scraping des actualités GFZ Online...\n")
    print(f"📍 URL: {BASE_URL}")
    print(f"📄 Pages à scraper: 9\n")
    
    # Demander confirmation
    reponse = input("Voulez-vous continuer? (o/n): ")
    if reponse.lower() != 'o':
        print("Annulé.")
        exit()
    
    print("\n" + "="*60)
    print("DÉBUT DU SCRAPING")
    print("="*60 + "\n")
    
    # Scraper toutes les pages
    actualites = scraper_toutes_pages(9)
    
    print("\n" + "="*60)
    print("FIN DU SCRAPING")
    print("="*60 + "\n")
    
    if actualites:
        # Sauvegarder en JSON
        sauvegarder_json(actualites)
        
        # Générer le SQL
        generer_sql(actualites)
        
        print(f"\n✨ Terminé! {len(actualites)} actualités extraites.")
        print(f"📁 Fichiers générés:")
        print(f"   - actualites_export.json")
        print(f"   - actualites_import.sql")
    else:
        print("\n❌ Aucune actualité trouvée.")
        print("💡 Vérifiez:")
        print("   - La connexion internet")
        print("   - Que l'URL est correcte")
        print("   - Que le site est accessible")
