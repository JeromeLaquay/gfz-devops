#!/usr/bin/env python3
"""
Script pour corriger les titres dans le fichier JSON existant
en réextrayant les titres corrects depuis les URLs
"""

import json
import requests
from bs4 import BeautifulSoup
import re
import time

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
            if titre_texte and titre_texte != "Groupe Français des Zéolithes" and len(titre_texte) > 5:
                return titre_texte
        
        # Fallback : utiliser le title de la page
        title_tag = soup.find('title')
        if title_tag:
            titre_complet = title_tag.get_text()
            if ' - ' in titre_complet:
                titre_extrait = titre_complet.split(' - ')[0].strip()
                if titre_extrait and titre_extrait != "Groupe Français des Zéolithes":
                    return titre_extrait
        
        return None
    except Exception as e:
        print(f"  ⚠️  Erreur pour {url}: {e}")
        return None

def corriger_fichier_json(fichier_entree, fichier_sortie):
    """Corrige les titres dans le fichier JSON"""
    print("🔧 Correction des titres dans le fichier JSON...\n")
    
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"📋 {len(articles)} articles à corriger\n")
    
    # Extraire les URLs depuis le contenu ou utiliser une liste
    # Pour l'instant, on va devoir reconstruire les URLs depuis les IDs dans les contenus
    # Ou utiliser une liste fournie
    
    print("⚠️  Ce script nécessite les URLs des articles pour corriger les titres.")
    print("💡 Solution recommandée :")
    print("   1. Utilisez extraire-tous-liens.js pour obtenir tous les liens")
    print("   2. Utilisez extraire-depuis-liens.py avec la liste complète")
    print("   3. Cela générera un nouveau JSON avec les bons titres")

if __name__ == "__main__":
    print("⚠️  Pour corriger les titres, il faut réextraire depuis les URLs.")
    print("💡 Utilisez plutôt :")
    print("   1. Obtenez tous les liens avec extraire-tous-liens.js")
    print("   2. Utilisez extraire-depuis-liens.py avec la liste complète")
    print("   3. Cela générera un nouveau JSON et SQL avec les bons titres")
