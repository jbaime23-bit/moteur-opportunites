import streamlit as st
from tavily import TavilyClient
from groq import Groq
import urllib.parse

# 1. Configuration de la page
st.set_page_config(page_title="Portail Opportunités & Urgences", page_icon="🌍", layout="centered")
st.title("🌍 Moteur IA : Emplois, Opportunités & Pharmacies")

# 2. Récupération sécurisée des clés depuis Streamlit Secrets
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# 3. Sélecteur de mode et situation géographique
col1, col2 = st.columns(2)

with col1:
    categorie = st.selectbox(
        "Que recherchez-vous ?",
        [
            "💼 Offres d'emploi & Recrutements",
            "🚀 Bourses, Financements & Appels d'offres",
            "💊 Pharmacies de garde"
        ]
    )

with col2:
    localisation = st.text_input("Ville ou Quartier :", value="Ouagadougou", placeholder="Ex: Bobo-Dioulasso, Gounghin...")

# 4. Champ de recherche spécifique
if categorie == "💊 Pharmacies de garde":
    requete_utilisateur = st.text_input(
        "Précisez votre besoin (optionnel) :",
        placeholder="Ex: pharmacie ouverte maintenant près de Gounghin"
    )
else:
    requete_utilisateur = st.text_input(
        "Mots-clés de votre recherche :",
        placeholder="Ex: technicien électricien, bourse master, ONG..."
    )

# 5. Exécution de la recherche
if st.button("Lancer la recherche", type="primary"):
    with st.spinner("Analyse des sources en temps réel..."):
        try:
            if categorie == "💊 Pharmacies de garde":
                requete_finale = f"pharmacies de garde {localisation} {requete_utilisateur} adresse téléphone"
                prompt_systeme = (
                    "Tu es un assistant d'urgence médicale précis. À partir des sources fournies, "
                    "liste clairement les pharmacies de garde trouvées pour la zone demandée. "
                    "Pour chaque pharmacie, indique : le NOM exact, le QUARTIER/ADRESSE, et le NUMÉRO DE TÉLÉPHONE si disponible. "
                    "Cite tes sources avec, [2], etc. Si la liste n'est pas à jour ou introuvable, précise-le clairement."
                )
            elif categorie == "💼 Offres d'emploi & Recrutements":
                requete_finale = f"offre emploi recrutement {requete_utilisateur} {localisation} date limite"
                prompt_systeme = (
                    "Tu es un chasseur de têtes et conseiller en emploi. À partir des sources fournies, "
                    "présente les offres d'emploi pertinentes sous forme de liste claire : "
                    "Intitulé du poste, Entreprise/Structure, Lieu, et Date limite de candidature. "
                    "Cite toujours les liens sources avec, [2], etc."
                )
            else:
                requete_finale = f"opportunité financement bourse appel d'offres {requete_utilisateur} {localisation}"
                prompt_systeme = (
                    "Tu es un expert en veille stratégique et opportunités. Résume les bourses, subventions ou "
                    "appels d'offres trouvés en précisant : le Titre, l'Organisme, les Conditions principales et la Date limite. "
                    "Cite toujours tes sources avec, [2], etc."
                )

            resultats_web = tavily.search(query=requete_finale, search_depth="advanced", max_results=6)

            contexte = ""
            sources = []
            for index, resultat in enumerate(resultats_web["results"], start=1):
                contexte += f"Source [{index}] ({resultat['url']}):\n{resultat['content']}\n\n"
                sources.append(f"[{index}] [{resultat['title']}]({resultat['url']})")

            reponse_ia = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt_systeme},
                    {"role": "user", "content": f"Zone : {localisation}\nDemande : {requete_utilisateur}\n\nSources :\n{contexte}"}
                ],
                temperature=0.1
            )

            st.markdown("### 📋 Résultats de la recherche")
            st.write(reponse_ia.choices[0].message.content)

            if categorie == "💊 Pharmacies de garde" and localisation:
                query_maps = urllib.parse.quote(f"Pharmacie {requete_utilisateur} {localisation}")
                lien_maps = f"https://google.com{query_maps}"
                st.link_button("📍 Voir les pharmacies sur la carte (Google Maps)", lien_maps)

            with st.expander("🔗 Voir les sources officielles consultées"):
                for source in sources:
                    st.markdown(f"- {source}")

        except Exception as e:
            st.error(f"Erreur lors de la recherche : {e}")
            
