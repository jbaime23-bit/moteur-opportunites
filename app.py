import streamlit as st
from tavily import TavilyClient
from groq import Groq
import urllib.parse

st.set_page_config(
    page_title="Portail IA : Emplois, Opportunités & Pharmacies",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp {background-color: #f4f7f6; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;}
    .hero-header {background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 25px 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;}
    .hero-header h1 {font-size: 1.6rem; font-weight: 700; margin: 0 0 8px 0; color: #ffffff;}
    .hero-header p {font-size: 0.95rem; margin: 0; color: #d1e8e2;}
    .promo-banner {background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%); color: white; padding: 14px 18px; border-radius: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;}
    .promo-banner a {background-color: white; color: #ff5e62; padding: 6px 12px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 0.85rem;}
    .side-ad-box {background-color: #ffffff; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 20px 12px; text-align: center; min-height: 220px; display: flex; flex-direction: column; justify-content: center; align-items: center;}
    .stButton > button {width: 100%; background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%); color: white; font-weight: bold; border: none; padding: 12px 20px; border-radius: 10px;}
    .result-card {background-color: white; padding: 20px; border-radius: 12px; border-left: 5px solid #00b09b; margin-top: 15px;}
</style>
""", unsafe_allow_html=True)

tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

col_centre, col_droite = st.columns([2.5, 1])

col_droite.markdown('<div class="side-ad-box"><b>PUBLICITÉ</b><br><br>Espace publicitaire disponible (Côté Droit)</div>', unsafe_allow_html=True)

with col_centre:
    st.markdown('<div class="hero-header"><h1>🌍 Portail IA : Emplois & Urgences</h1><p>Trouvez instantanément les offres d\'emploi, financements et pharmacies de garde près de chez vous.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="promo-banner"><div><strong>📚 TechLibrairie</strong><br>Guides techniques, livres numériques & ressources pro.</div><a href="https://techlibrairie.com" target="_blank">Découvrir</a></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    categorie = c1.selectbox("Catégorie de recherche", ["💼 Offres d'emploi & Recrutements", "🚀 Bourses, Financements & Appels d'offres", "💊 Pharmacies de garde"])
    localisation = c2.text_input("Ville ou Quartier", value="Ouagadougou", placeholder="Ex: Bobo-Dioulasso, Gounghin...")

    if categorie == "💊 Pharmacies de garde":
        requete_utilisateur = st.text_input("Nom de la pharmacie ou précision (optionnel)", placeholder="Ex: Pharmacie du Progrès, Gounghin...")
    else:
        requete_utilisateur = st.text_input("Mots-clés de votre recherche", placeholder="Ex: technicien électricien, bourse master, ONG...")

    if st.button("🔍 Lancer la recherche maintenant"):
        with st.spinner("Recherche et analyse en cours..."):
            try:
                if categorie == "💊 Pharmacies de garde":
                    requete_finale = f"pharmacies de garde {localisation} {requete_utilisateur} adresse téléphone"
                    prompt_systeme = "Liste clairement les pharmacies de garde trouvées avec le NOM, QUARTIER/ADRESSE et TÉLÉPHONE. Cite tes sources avec, [2]."
                elif categorie == "💼 Offres d'emploi & Recrutements":
                    requete_finale = f"offre emploi recrutement {requete_utilisateur} {localisation} date limite"
                    prompt_systeme = "Présente les offres d'emploi pertinentes : Intitulé, Entreprise, Lieu et Date limite. Cite tes sources avec, [2]."
                else:
                    requete_finale = f"opportunité financement bourse appel d'offres {requete_utilisateur} {localisation}"
                    prompt_systeme = "Résume les bourses, subventions ou appels d'offres trouvés : Titre, Organisme, Conditions et Date limite. Cite tes sources avec, [2]."

                resultats_web = tavily.search(query=requete_finale, search_depth="advanced", max_results=6)
                contexte = ""
                sources = []
                for index, resultat in enumerate(resultats_web["results"], start=1):
                    contexte += f"Source [{index}] ({resultat['url']}):\n{resultat['content']}\n\n"
                    sources.append(f"[{index}] [{resultat['title']}]({resultat['url']})")

                reponse_ia = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": prompt_systeme},
                        {"role": "user", "content": f"Zone : {localisation}\nDemande : {requete_utilisateur}\n\nSources :\n{contexte}"}
                    ],
                    temperature=0.1
                )

                st.markdown("### 📋 Résultats trouvés")
                st.markdown(f'<div class="result-card">{reponse_ia.choices[0].message.content}</div>', unsafe_allow_html=True)

                if categorie == "💊 Pharmacies de garde":
                    terme_carte = f"Pharmacie {requete_utilisateur} {localisation}".strip()
                    lien_maps = f"https://google.com{urllib.parse.quote_plus(terme_carte)}"
                    st.markdown(f"<br>📍 **[Ouvrir l'itinéraire sur Google Maps]({lien_maps})**", unsafe_allow_html=True)

                with st.expander("🔗 Voir les sources officielles consultées"):
                    for source in sources:
                        st.markdown(f"- {source}")

            except Exception as e:
                st.error(f"Erreur lors de la recherche : {e}")
                
