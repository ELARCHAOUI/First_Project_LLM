import os
import json
import re
import google.generativeai as genai
import streamlit as st

# --- 1. CONFIGURATION DE LA CLÉ API ---
# Méthode sécurisée et recommandée : lire la clé depuis l'environnement.
# Assurez-vous d'avoir exécuté `export GOOGLE_API_KEY="..."` dans votre terminal.
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("La variable d'environnement GOOGLE_API_KEY n'a pas été trouvée.")
    st.error("Veuillez la définir dans votre terminal avant de lancer l'application.")
    st.stop()

# --- 2. LE PROMPT (NOTRE RECETTE SECRÈTE) ---
PROMPT_TEMPLATE = """
Tu es un assistant expert en traitement d'emails. Ton rôle est d'analyser l'email ci-dessous et d'extraire les informations dans un format JSON strict.

Le JSON doit contenir EXACTEMENT les clés suivantes : "intention", "nom_produit", "numero_client", "urgence".
- L'intention doit être une de ces valeurs : "demande_devis", "question_technique", "reclamation", "suivi_commande".
- L'urgence doit être une de ces valeurs : "faible", "moyenne", "elevee".

---
Exemple 1 :
EMAIL : \"\"\"
Sujet: Question concernant votre catalogue

Bonjour à toute l'équipe,
Je suis en train de parcourir votre site et le modèle de chaise "ErgoChair Pro" a attiré mon attention. Serait-il possible d'obtenir un devis détaillé pour une commande de 12 unités ? C'est pour équiper nos nouveaux bureaux et nous en aurions besoin assez rapidement.
Merci d'avance pour votre retour.
Cordialement,
Jean Dupont
\"\"\"
JSON :
```json
{{
  "intention": "demande_devis",
  "nom_produit": "ErgoChair Pro",
  "numero_client": null,
  "urgence": "moyenne"
}}
Exemple 2 :
EMAIL : \"\"\"
Sujet: Problème avec ma commande

Bonjour,
Le 'Routeur-XG' que j'ai reçu hier ne s'allume pas du tout. C'est vraiment problématique, j'en ai besoin pour mon travail. Que dois-je faire ?
Cdt,
A. Martin
\"\"\"
JSON :
{{
  "intention": "reclamation",
  "nom_produit": "Routeur-XG",
  "numero_client": null,
  "urgence": "elevee"
}}
Email à analyser :
EMAIL : \"\"\"
{email_text}
\"\"\"
JSON :
"""

#--- 3. LA FONCTION (NOTRE USINE AMÉLIORÉE) ---


def extract_info_from_email(email_text: str) -> str:
    """
    Prend un email en entrée et retourne une réponse du modèle.
    """
    import google.generativeai as genai
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    # Utilise .format() pour insérer l'email dans le prompt
    prompt = PROMPT_TEMPLATE.format(email_text=email_text)

    response = model.generate_content(prompt)
    return response.text
#--- 4. INTERFACE STREAMLIT ---


st.title("Extracteur d'informations d'emails (propulsé par Gemini)")

#Zone de texte pour entrer l'email


email_input = st.text_area("Collez votre email ici :", height=200)

#Bouton pour lancer l'analyse


if st.button("Analyser l'email"):
    if email_input:
        st.info("Analyse en cours...")
    try:
        reponse = extract_info_from_email(email_input)
        st.success("Réponse du modèle :")
        st.write(reponse)
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
else:
    st.warning("Veuillez entrer un email.")