#!/usr/bin/env python3
"""
Script pour télécharger toutes les images du fichier SQL
et les remplacer par des data URIs (base64)
"""

import re
import requests
import base64
from urllib.parse import urljoin, urlparse
import mimetypes
import time
from pathlib import Path

def detecter_type_mime(url, contenu):
    """Détecte le type MIME d'une image"""
    # D'abord essayer depuis l'extension de l'URL
    type_mime, _ = mimetypes.guess_type(url)
    
    if type_mime and type_mime.startswith('image/'):
        return type_mime
    
    # Sinon, détecter depuis le contenu (magic bytes)
    if contenu.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    elif contenu.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif contenu.startswith(b'GIF87a') or contenu.startswith(b'GIF89a'):
        return 'image/gif'
    elif contenu.startswith(b'RIFF') and b'WEBP' in contenu[:12]:
        return 'image/webp'
    
    # Par défaut
    return 'image/png'

def telecharger_et_convertir(url):
    """Télécharge une image et la convertit en base64"""
    try:
        print(f"  📥 Téléchargement: {url}")
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()
        
        contenu = response.content
        type_mime = detecter_type_mime(url, contenu)
        
        base64_data = base64.b64encode(contenu).decode('utf-8')
        data_uri = f"data:{type_mime};base64,{base64_data}"
        
        print(f"  ✅ Converti en {type_mime} ({len(contenu)} bytes)")
        return data_uri
        
    except Exception as e:
        print(f"  ⚠️  Erreur pour {url}: {e}")
        return None

def extraire_urls_images(contenu_sql):
    """Extrait toutes les URLs d'images du fichier SQL"""
    urls = set()
    base_url = "https://gfz-online.fr"
    
    # Pattern pour les URLs dans la colonne image (après le contenu, avant CURRENT_TIMESTAMP)
    # Format: ', 'https://...', CURRENT_TIMESTAMP) ou ', NULL, CURRENT_TIMESTAMP)
    pattern_colonne = r",\s*'((?:https?://[^']+\.(?:jpg|jpeg|png|gif|webp|JPG|JPEG|PNG|GIF|WEBP)[^']*))'\s*,\s*CURRENT_TIMESTAMP"
    matches = re.findall(pattern_colonne, contenu_sql, re.IGNORECASE)
    for url in matches:
        urls.add(url)
    
    # Pattern pour les images dans le contenu HTML (balises img)
    pattern_html = r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|JPG|JPEG|PNG|GIF|WEBP)[^"\']*)["\']'
    matches = re.findall(pattern_html, contenu_sql, re.IGNORECASE)
    
    # Convertir les URLs relatives en absolues
    for url in matches:
        if url.startswith('http'):
            urls.add(url)
        elif url.startswith('/'):
            urls.add(urljoin(base_url, url))
        else:
            urls.add(urljoin(base_url, '/' + url))
    
    # Pattern pour les URLs absolues dans le contenu (hors balises)
    pattern_general = r'https?://[^\s<>"\']+\.(?:jpg|jpeg|png|gif|webp|JPG|JPEG|PNG|GIF|WEBP)(?:\?[^\s<>"\']*)?'
    matches = re.findall(pattern_general, contenu_sql, re.IGNORECASE)
    urls.update(matches)
    
    # Pattern pour les URLs relatives commençant par /images/
    # Utiliser des guillemets simples pour la chaîne externe pour éviter les conflits avec les guillemets doubles
    pattern_relatives = r"'([/]images/[^\s<>""']+\.(?:jpg|jpeg|png|gif|webp|JPG|JPEG|PNG|GIF|WEBP)[^\s<>""']*)'"
    matches = re.findall(pattern_relatives, contenu_sql, re.IGNORECASE)
    for url in matches:
        if url.startswith('/'):
            urls.add(urljoin(base_url, url))
    
    return sorted(list(urls))

def remplacer_urls_par_base64(contenu_sql, mapping_urls):
    """Remplace toutes les URLs par leurs équivalents base64"""
    contenu_modifie = contenu_sql
    base_url = "https://gfz-online.fr"
    
    # Trier par longueur décroissante pour éviter les remplacements partiels
    urls_triees = sorted(mapping_urls.items(), key=lambda x: len(x[0]), reverse=True)
    
    for url_originale, data_uri in urls_triees:
        # Échapper les caractères spéciaux pour la regex
        url_escape = re.escape(url_originale)
        
        # Pattern pour la colonne image (avant CURRENT_TIMESTAMP)
        # Format: ', 'url', CURRENT_TIMESTAMP)
        pattern_colonne = f",\\s*'{url_escape}'\\s*,\\s*CURRENT_TIMESTAMP"
        contenu_modifie = re.sub(
            pattern_colonne,
            f", '{data_uri}', CURRENT_TIMESTAMP",
            contenu_modifie,
            flags=re.IGNORECASE
        )
        
        # Remplacer dans les balises img du contenu HTML
        # Pattern: src="url" ou src='url'
        pattern_img = f'(<img[^>]+src=["\']){url_escape}(["\'])'
        contenu_modifie = re.sub(
            pattern_img,
            f'\\1{data_uri}\\2',
            contenu_modifie,
            flags=re.IGNORECASE
        )
        
        # Remplacer les URLs dans les attributs href ou autres
        pattern_attribut = f'(["\']){url_escape}(["\'])'
        contenu_modifie = re.sub(
            pattern_attribut,
            f'\\1{data_uri}\\2',
            contenu_modifie,
            flags=re.IGNORECASE
        )
        
        # Remplacer aussi les URLs relatives correspondantes
        url_relative = url_originale.replace(base_url, '')
        if url_relative != url_originale and url_relative.startswith('/'):
            # Pattern pour URL relative dans la colonne image
            pattern_colonne_rel = f",\\s*'{re.escape(url_relative)}'\\s*,\\s*CURRENT_TIMESTAMP"
            contenu_modifie = re.sub(
                pattern_colonne_rel,
                f", '{data_uri}', CURRENT_TIMESTAMP",
                contenu_modifie,
                flags=re.IGNORECASE
            )
            
            # Pattern pour URL relative dans les balises img
            pattern_img_rel = f'(<img[^>]+src=["\']){re.escape(url_relative)}(["\'])'
            contenu_modifie = re.sub(
                pattern_img_rel,
                f'\\1{data_uri}\\2',
                contenu_modifie,
                flags=re.IGNORECASE
            )
    
    return contenu_modifie

def convertir_images_sql(fichier_entree, fichier_sortie):
    """Fonction principale"""
    print("🖼️  Conversion des images en base64\n")
    
    # Lire le fichier SQL
    print(f"📖 Lecture de {fichier_entree}...")
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        contenu_sql = f.read()
    
    # Extraire toutes les URLs d'images
    print("\n🔍 Extraction des URLs d'images...")
    urls = extraire_urls_images(contenu_sql)
    print(f"📋 {len(urls)} images trouvées\n")
    
    if not urls:
        print("⚠️  Aucune image trouvée dans le fichier SQL")
        return
    
    # Télécharger et convertir chaque image
    mapping_urls = {}
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        data_uri = telecharger_et_convertir(url)
        if data_uri:
            mapping_urls[url] = data_uri
        time.sleep(0.5)  # Pause pour éviter de surcharger le serveur
    
    print(f"\n✅ {len(mapping_urls)}/{len(urls)} images converties avec succès\n")
    
    # Remplacer les URLs dans le contenu SQL
    print("🔄 Remplacement des URLs par les data URIs...")
    contenu_modifie = remplacer_urls_par_base64(contenu_sql, mapping_urls)
    
    # Sauvegarder le fichier modifié
    print(f"💾 Sauvegarde dans {fichier_sortie}...")
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        f.write(contenu_modifie)
    
    print("\n✅ Conversion terminée !")
    print(f"📊 Statistiques:")
    print(f"   - Images trouvées: {len(urls)}")
    print(f"   - Images converties: {len(mapping_urls)}")
    print(f"   - Échecs: {len(urls) - len(mapping_urls)}")

if __name__ == "__main__":
    import sys
    
    fichier_entree = "actualites_import.sql"
    fichier_sortie = "actualites_import_base64.sql"
    
    if len(sys.argv) > 1:
        fichier_entree = sys.argv[1]
    if len(sys.argv) > 2:
        fichier_sortie = sys.argv[2]
    
    convertir_images_sql(fichier_entree, fichier_sortie)
