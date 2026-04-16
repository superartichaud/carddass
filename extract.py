import os
import base64
import hashlib
from bs4 import BeautifulSoup

# On ouvre ton fichier téléchargé
with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

os.makedirs('images', exist_ok=True)

seen_hashes = set()
i = 1

print("Analyse des images en cours...")

for img in soup.find_all('img'):
    src = img.get('src')
    if src and 'data:image' in src:
        try:
            header, data_str = src.split(',', 1)
            image_data = base64.b64decode(data_str)
            
            # On calcule l'empreinte unique de l'image
            img_hash = hashlib.md5(image_data).hexdigest()
            
            if img_hash not in seen_hashes:
                seen_hashes.add(img_hash)
                ext = header.split('/')[1].split(';')[0]
                if ext == 'jpeg': ext = 'jpg'
                
                filename = f'images/carte_{i:03d}.{ext}'
                with open(filename, 'wb') as f_img:
                    f_img.write(image_data)
                
                # On met à jour le lien dans le HTML
                img['src'] = filename
                i += 1
            else:
                # Si c'est un doublon, on supprime carrément la balise image du HTML
                img.decompose() 
                
        except Exception as e:
            pass

# Nettoyage final du HTML : on ne garde que les balises <img> dans le body
new_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Collection Propre</title>
    <style>
        body { background: #1a1a1a; display: flex; flex-direction: column; align-items: center; gap: 20px; padding: 20px; }
        img { max-width: 90%; height: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-radius: 10px; }
    </style>
</head>
<body>
"""

for img in soup.find_all('img'):
    if 'images/' in img.get('src', ''):
        new_html += str(img) + "\n"

new_html += "</body>\</html>"

with open('index_propre.html', 'w', encoding='utf-8') as f_out:
    f_out.write(new_html)

print(f"Terminé ! {i-1} images uniques extraites dans le dossier /images.")