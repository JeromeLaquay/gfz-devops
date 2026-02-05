#!/usr/bin/env python3
"""
Script pour importer les actualités depuis un fichier JSON
vers l'API du nouveau site
"""

import json
import requests
import sys
from datetime import datetime

API_BASE_URL = "http://localhost:8080/api"  # À modifier selon l'environnement
ADMIN_TOKEN = ""  # Token JWT d'un administrateur

def parser_date(date_str):
    """Parse une date en format ISO"""
    if not date_str:
        return None
    
    # Formats de date courants
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d %B %Y",
        "%B %d, %Y",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).isoformat()
        except:
            continue
    
    return None

def importer_article(article, token):
    """Importe un article via l'API"""
    url = f"{API_BASE_URL}/articles"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Préparer les données
    data = {
        "titre": article.get("titre", ""),
        "contenu": article.get("contenu", ""),
        "image": article.get("image")
    }
    
    # Ajouter la date si disponible
    date_creation = parser_date(article.get("dateCreation"))
    if date_creation:
        # Note: L'API pourrait ne pas accepter la date directement
        # À adapter selon votre API
        pass
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur pour '{article.get('titre', 'Sans titre')}': {e}")
        if hasattr(e.response, 'text'):
            print(f"   Réponse: {e.response.text}")
        return None

def importer_depuis_json(filename, token):
    """Importe tous les articles depuis un fichier JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {filename} non trouvé")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {e}")
        return
    
    print(f"📦 {len(articles)} articles à importer\n")
    
    if not token:
        print("⚠️  Token admin requis. Obtenez-le en vous connectant à l'API.")
        token = input("Entrez votre token JWT: ").strip()
    
    succes = 0
    echecs = 0
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] Import de: {article.get('titre', 'Sans titre')[:50]}...")
        
        result = importer_article(article, token)
        if result:
            print(f"  ✅ Importé (ID: {result.get('id', 'N/A')})")
            succes += 1
        else:
            echecs += 1
        
        # Pause pour ne pas surcharger l'API
        import time
        time.sleep(0.5)
    
    print(f"\n✨ Terminé!")
    print(f"   ✅ Succès: {succes}")
    print(f"   ❌ Échecs: {echecs}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import-actualites-api.py <fichier.json> [token]")
        print("Exemple: python import-actualites-api.py actualites_export.json")
        sys.exit(1)
    
    filename = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else ADMIN_TOKEN
    
    # Modifier l'URL de l'API si nécessaire
    if len(sys.argv) > 3:
        API_BASE_URL = sys.argv[3]
    
    importer_depuis_json(filename, token)
