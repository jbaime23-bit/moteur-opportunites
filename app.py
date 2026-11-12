import streamlit as st
from tavily import TavilyClient
from groq import Groq
import urllib.parse

# 1. Configuration de la page
st.set_page_config(
    page_title="Portail IA : Emplois, Opportunités & Pharmacies",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Design CSS Moderne (Masque l'aspect amateur et stylise l'interface)
st.markdown("""
<style>
    /* Masquer les éléments par défaut de Streamlit (menu, footer, barre du haut) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Fond général propre */
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* En-tête moderne avec dégradé */
    .hero-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 25px 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .hero-header h1 {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        color: #ffffff;
    }
    .hero-header p {
        font-size: 0.95rem;
        margin: 0;
        color: #d1e8e2;
    }

    /* Bannière publicitaire TechLibrairie stylisée */
    .promo-banner {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 10px rgba(255, 94, 98, 0.25);
        font-size: 0.9rem;
    }
    .promo-banner a {
        background-color: white;
        color: #ff5e62;
        padding: 6px 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.85rem;
        white-space: nowrap;
        margin-left: 10px;
    }

    /* Bouton de recherche principal moderne */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
        color: white;
        font-weight: bold;
        font-size: 1.05rem;
        border: none;
        padding: 12px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 176, 155, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 176, 155, 0.4);
    }

    /* Carte de résultats */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border-left: 5px solid #00b09b;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Affichage de l'en-tête personnalisé
st.markdown("""
<div class="hero-header">
    <h1>🌍 Portail IA : Emplois & Urgences</h1>
    <p>Trouvez instantanément les offres d'emploi, financements et pharmacies de garde près de chez vous.</p>
</div>
""", unsafe_allow_html=True)

# 4. Affichage de la bannière TechLibrairie
st.markdown("""
<div class="promo-banner">
    <div><strong>📚 TechLibrairie</strong><br>Guides techniques, livres numériques & ressources pro.</div>
    <a href="https://techlibrairie.com" target="_blank">Découvrir</a>
</div>
""", unsafe_allow_html=True)

# 5. Récupération sécurisée des clés API
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# 6. Zone de recherche
col1, col2 = st.columns(2)

with col1:
    categorie = st.selectbox(
        "Catégorie de recherche",
        [
            "💼 Offres d'emploi & Recrutements",
            "🚀 Bourses, Financements & Appels d'offres",
            "💊 Pharmacies de garde"
        ]
    )

with col2:
    localisation = st.text_input("Ville ou Quartier", value="Ouagadougou", placeholder="Ex: Bobo-Dioulasso, Gounghin...")

if categorie == "💊 Pharmacies de garde":
    requete_utilisateur = st.text_input(
        "Nom de la pharmacie ou précision (optionnel)",
        placeholder="Ex: Pharmacie du Progrès, Gounghin..."
    )
else:
    requete_utilisateur = st.text_input(
        "Mots-clés de votre recherche",
        placeholder="Ex: technicien électricien, bourse master, ONG..."
    )

# 7. Exécution et affichage des résultats
if st.button("🔍 Lancer la recherche maintenant"):
    with st.spinner("Recherche et analyse des meilleures sources en cours..."):
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
                query_maps = urllib.parse.quote_plus(terme_carte)
                lien_maps = f"https://google.com{query_maps}"
                st.markdown(f"<br>📍 **[Ouvrir l'itinéraire sur Google Maps]({lien_maps})**", unsafe_allow_html=True)

            with st.expander("🔗 Voir les sources officielles consultées"):
                for source in sources:
                    st.markdown(f"- {source}")

        except Exception as e:
            st.error(f"Erreur lors de la recherche : {e}")
            
