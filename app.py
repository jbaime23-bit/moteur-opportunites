import streamlit as st
from tavily import TavilyClient
from groq import Groq
import urllib.parse

# 1. Configuration de la page en mode large pour accueillir les côtés
st.set_page_config(
    page_title="Portail IA : Emplois, Opportunités & Pharmacies",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Design CSS Moderne + Emplacements Publicitaires
st.markdown("""
<style>
    /* Masquer les éléments par défaut de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}

    .stApp {
        background-color: #f4f7f6;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* En-tête moderne */
    .hero-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 22px 18px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .hero-header h1 {
        font-size: 1.55rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        color: #ffffff;
    }
    .hero-header p {
        font-size: 0.9rem;
        margin: 0;
        color: #d1e8e2;
    }

    /* Bannière principale TechLibrairie */
    .promo-banner {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 18px;
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

    /* Encarts Publicitaires Latéraux (Gauche et Droite) */
    .side-ad {
        background-color: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .side-ad h4 {
        color: #1e293b;
        font-size: 0.95rem;
        margin: 0 0 6px 0;
    }
    .side-ad p {
        color: #64748b;
        font-size: 0.8rem;
        margin: 0 0 10px 0;
    }
    .side-ad a {
        display: inline-block;
        background-color: #203a43;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: bold;
    }

    /* Encart Publicitaire Bas de Page */
    .bottom-ad {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.2);
    }
    .bottom-ad a {
        display: inline-block;
        margin-top: 8px;
        background-color: #fbbf24;
        color: #1e293b;
        padding: 7px 16px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.85rem;
    }

    /* Bouton de recherche principal */
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

# 3. Récupération sécurisée des clés API
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# 4. Découpage en 3 colonnes : Côté Gauche | Centre (Moteur) | Côté Droit
col_gauche, col_centre, col_droite = st.columns([1, 2.4, 1])

# --- COLONNE GAUCHE (Publicité latérale 1) ---
with col_gauche:
    st.markdown("""
    <div class="side-ad">
        <h4>📘 Espace Pub Gauche</h4>
        <p>Faites connaître vos formations, livres ou services ici.</p>
        <a href="https://techlibrairie.com" target="_blank">Voir les offres</a>
    </div>
    """, unsafe_allow_html=True)

# --- COLONNE CENTRALE (Moteur de recherche) ---
with col_centre:
    st.markdown("""
    <div class="hero-header">
        <h1>🌍 Portail IA : Emplois & Urgences</h1>
        <p>Offres d'emploi, financements et pharmacies de garde en temps réel.</p>
    </div>
    """, unsafe_allow_html=True)

    # Bannière TechLibrairie en haut
    st.markdown("""
    <div class="promo-banner">
        <div><strong>📚 TechLibrairie</strong><br>Guides techniques, livres numériques & ressources pro.</div>
        <a href="https://techlibrairie.com" target="_blank">Découvrir</a>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        categorie = st.selectbox(
            "Catégorie de recherche",
            [
                "💼 Offres d'emploi & Recrutements",
                "🚀 Bourses, Financements & Appels d'offres",
                "💊 Pharmacies de garde"
            ]
        )
    with c2:
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

    if st.button("🔍 Lancer la recherche maintenant"):
        with st.spinner("Recherche et analyse des meilleures sources en cours..."):
            try:
                if categorie == "💊 Pharmacies de garde":
                    requete_finale = f"pharmacies de garde {localisation} {requete_utilisateur} adresse téléphone"
                    prompt_systeme = (
                        "Tu es un assistant d'urgence médicale précis. À partir des sources fournies, "
                        "liste clairement les pharmacies de garde trouvées pour la zone demandée. "
                        "Pour chaque pharmacie, indique : le NOM exact, le QUARTIER/ADRESSE, et le NUMÉRO DE TÉLÉPHONE si disponible. "
                        "Cite tes sources avec,, etc. Si la liste n'est pas à jour ou introuvable, précise-le clairement."
                    )
                elif categorie == "💼 Offres d'emploi & Recrutements":
                    requete_finale = f"offre emploi recrutement {requete_utilisateur} {localisation} date limite"
                    prompt_systeme = (
                        "Tu es un chasseur de têtes et conseiller en emploi. À partir des sources fournies, "
                        "présente les offres d'emploi pertinentes sous forme de liste claire : "
                        "Intitulé du poste, Entreprise/Structure, Lieu, et Date limite de candidature. "
                        "Cite toujours les liens sources avec,, etc."
                    )
                else:
                    requete_finale = f"opportunité financement bourse appel d'offres {requete_utilisateur} {localisation}"
                    prompt_systeme = (
                        "Tu es un expert en veille stratégique et opportunités. Résume les bourses, subventions ou "
                        "appels d'offres trouvés en précisant : le Titre, l'Organisme, les Conditions principales et la Date limite. "
                        "Cite toujours tes sources avec,, etc."
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
                st.markdown(f'<div class="result-card">{reponse_ia.choices.message.content}</div>', unsafe_allow_html=True)

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

