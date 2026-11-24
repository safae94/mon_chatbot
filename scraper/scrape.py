# 1. Importer les outils
import requests                     # télécharger une page web
from bs4 import BeautifulSoup       # lire le HTML de la page

# 2. L'adresse de la page à récupérer
URL = "https://en.wikipedia.org/wiki/Web_scraping"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)

  # se présenter comme un navigateur


if response.status_code == 200:          # 200 = la page est bien arrivée
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Garder le titre + le texte de l'article seulement
    final_text = soup.title.text + "\n"
    main_content = soup.find(id="mw-content-text")
    final_text += main_content.get_text(separator="\n", strip=True)

    # 5. Enregistrer dans le dossier knowledge_base
    with open("../knowledge_base/webscraping.txt", "w", encoding="utf-8") as file:
        file.write(final_text)
    print("Page enregistrée dans knowledge_base/webscraping.txt")
else:
    print("Erreur : la page n'a pas répondu")