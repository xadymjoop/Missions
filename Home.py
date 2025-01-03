import streamlit as st
from database import get_db_connection

# Configuration de la page Streamlit (DOIT ÊTRE LA PREMIÈRE COMMANDE)
st.set_page_config(layout="wide", page_title="Plateforme de Gestion des Missions", page_icon="🌍")

# Charger FontAwesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)

# Charger le fichier CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Appliquer le CSS
load_css()

# Fonction pour récupérer le nombre de missions en cours
def get_missions_en_cours():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM missions WHERE statut = 'En cours'")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Fonction pour récupérer le nombre d'utilisateurs actifs
def get_utilisateurs_actifs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM utilisateurs")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Gestion de la session utilisateur
if 'utilisateur' not in st.session_state:
    st.session_state['utilisateur'] = None
if 'role' not in st.session_state:
    st.session_state['role'] = None

# Sidebar pour la navigation
st.sidebar.title("Navigation")
if st.session_state['utilisateur']:
    st.sidebar.write(f"Connecté en tant que : {st.session_state['utilisateur']} ({st.session_state['role']})")
    if st.sidebar.button("Se déconnecter"):
        st.session_state['utilisateur'] = None
        st.session_state['role'] = None
        st.sidebar.success("Déconnecté avec succès")
        st.rerun()  # Recharger la page après déconnexion
    
    # Afficher le lien "Tableau de Bord" pour tous les utilisateurs
    st.sidebar.page_link("pages/Tableau_de_Bord.py", label="Tableau de Bord")
    
    # Afficher les liens "Créer une Mission" et "Détails de la Mission" pour tous les utilisateurs
    st.sidebar.page_link("pages/Créer_Mission.py", label="Créer une Mission")
    st.sidebar.page_link("pages/Détails_Mission.py", label="Détails de la Mission")
    
    # Afficher les liens "Supprimer une Mission" et "Gestion des Utilisateurs" uniquement pour l'administrateur
    if st.session_state['role'] == "Administrateur":
        st.sidebar.page_link("pages/Supprimer_Mission.py", label="Supprimer une Mission")
        st.sidebar.page_link("pages/Gestion_Utilisateurs.py", label="Gestion des Utilisateurs")
else:
    st.sidebar.write("Veuillez vous connecter pour accéder aux fonctionnalités.")
    st.sidebar.page_link("pages/Connexion.py", label="Connexion")

# Page d'accueil avec style Hero et superposition de l'image
st.markdown("""
    <div class="hero">
        <img src="https://europe.wetlands.org/wp-content/uploads/sites/6/2024/04/AdobeStock_249282402-1920x1050.jpeg" alt="Hero Image" class="hero-image">
        <div class="hero-content">
            <h1>Plateforme de Gestion des Missions</h1>
            <p>Bienvenue sur la plateforme de gestion des missions.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Ajouter des statistiques ou des indicateurs centrés
st.markdown("""
    <div class="metrics">
        <div class="metric">
            <h3><i class="fas fa-tasks"></i> Missions en cours</h3>
            <p>{}</p>
        </div>
        <div class="metric">
            <h3><i class="fas fa-users"></i> Utilisateurs actifs</h3>
            <p>{}</p>
        </div>
    </div>
""".format(get_missions_en_cours(), get_utilisateurs_actifs()), unsafe_allow_html=True)