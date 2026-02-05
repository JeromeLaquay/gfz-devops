#!/usr/bin/env python3
"""
Script pour corriger les titres dans le fichier SQL
en réextrayant les titres corrects depuis les URLs
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

BASE_URL = "https://gfz-online.fr"

def nettoyer_texte(texte):
    """Nettoie le texte HTML"""
    if not texte:
        return ""
    texte = re.sub(r'<[^>]+>', '', str(texte))
    texte = ' '.join(texte.split())
    return texte.strip()

def extraire_titre_correct(url):
    """Extrait le titre correct depuis l'URL"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Chercher dans l'article spécifiquement
        article_elem = soup.find('article', class_='item')
        if article_elem:
            titre_elem = article_elem.find('h1')
        else:
            component = soup.find('div', id='sp-component')
            if component:
                titre_elem = component.find('h1')
            else:
                titre_elem = soup.find('h1')
        
        if titre_elem:
            span_format = titre_elem.find('span', class_='post-format')
            if span_format:
                span_format.decompose()
            titre_texte = nettoyer_texte(titre_elem.get_text())
            if titre_texte and titre_texte != "Groupe Français des Zéolithes":
                return titre_texte
        
        # Fallback : utiliser le title de la page
        title_tag = soup.find('title')
        if title_tag:
            titre_complet = title_tag.get_text()
            if ' - ' in titre_complet:
                return titre_complet.split(' - ')[0].strip()
        
        return None
    except Exception as e:
        print(f"  ⚠️  Erreur pour {url}: {e}")
        return None

def corriger_fichier_sql(fichier_entree, fichier_sortie):
    """Corrige les titres dans le fichier SQL"""
    print("🔧 Correction des titres dans le fichier SQL...\n")
    
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Extraire toutes les URLs depuis le JSON si disponible
    # Sinon, on devra les extraire depuis le SQL ou les avoir en liste
    
    # Pour l'instant, on va chercher les patterns dans le SQL
    # et proposer une correction manuelle
    
    # Pattern pour trouver les INSERT avec titre incorrect
    pattern = r"INSERT INTO articles \(titre, contenu, image, date_creation\) VALUES\s*\n\s*\('Groupe Français des Zéolithes',"
    
    matches = list(re.finditer(pattern, contenu))
    
    if matches:
        print(f"⚠️  {len(matches)} articles avec titre incorrect trouvés")
        print("💡 Pour corriger automatiquement, il faut avoir la liste des URLs.")
        print("   Utilisez le script extraire-depuis-liens.py avec la liste complète des URLs.")
    else:
        print("✅ Aucun titre incorrect trouvé (ou format différent)")

if __name__ == "__main__":
    print("⚠️  Ce script nécessite la liste complète des URLs pour corriger automatiquement.")
    print("💡 Solution recommandée :")
    print("   1. Utilisez extraire-tous-liens.js dans le navigateur pour obtenir tous les liens")
    print("   2. Modifiez extraire-depuis-liens.py avec la liste complète")
    print("   3. Relancez l'extraction pour générer un nouveau SQL avec les bons titres")
    print("\n   Ou utilisez le script corrigé scrape-actualites-v2.py qui a été mis à jour.")
