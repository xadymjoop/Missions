import streamlit as st
from database import verifier_connexion
import os

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

# Contenu de la page
st.title("Connexion")
st.markdown("""
    <div class="stCard">
        <h2><i class="fas fa-sign-in-alt"></i> Connectez-vous</h2>
        <p>Veuillez entrer vos informations de connexion.</p>
    </div>
""", unsafe_allow_html=True)

def afficher_connexion():
    st.header("Connexion")
    
    # Formulaire de connexion
    with st.form("form_connexion"):
        nom = st.text_input("Nom d'utilisateur")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        # Bouton de soumission
        if st.form_submit_button("Se connecter"):
            if nom and mot_de_passe:  # Vérifier que les champs ne sont pas vides
                # Vérifier les informations de connexion
                role = verifier_connexion(nom, mot_de_passe)
                if role:
                    # Stocker les informations de l'utilisateur dans la session
                    st.session_state['utilisateur'] = nom
                    st.session_state['role'] = role
                    st.success(f"Connecté en tant que {nom} ({role})")
                    # Rediriger vers le tableau de bord
                    st.switch_page("pages/Tableau_de_bord.py")
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")
            else:
                st.warning("Veuillez remplir tous les champs.")

# Afficher le formulaire de connexion
afficher_connexion()