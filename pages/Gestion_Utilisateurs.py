import streamlit as st
from database import get_db_connection, hash_password, creer_utilisateur, supprimer_utilisateur
# Charger le fichier CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Appliquer le CSS
load_css()
def afficher_gestion_utilisateurs():
    # Vérifier si l'utilisateur est un administrateur
    if st.session_state.get('role') == "Administrateur":
        st.header("Gestion des Utilisateurs")
        
        # Ajouter un utilisateur
        st.subheader("Ajouter un Utilisateur")
        with st.form("form_ajouter_utilisateur"):
            nom_utilisateur = st.text_input("Nom d'utilisateur")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            role = st.selectbox("Rôle", ["Utilisateur", "Administrateur"])
            if st.form_submit_button("Ajouter l'utilisateur"):
                creer_utilisateur(nom_utilisateur, mot_de_passe, role)
                st.success(f"Utilisateur {nom_utilisateur} ajouté avec succès !")
        
        # Supprimer un utilisateur
        st.subheader("Supprimer un Utilisateur")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT nom FROM utilisateurs')
        utilisateurs = cursor.fetchall()
        conn.close()
        
        if utilisateurs:
            utilisateur_a_supprimer = st.selectbox("Choisir un utilisateur à supprimer", [u[0] for u in utilisateurs])
            if st.button("Supprimer l'utilisateur"):
                supprimer_utilisateur(utilisateur_a_supprimer)
                st.success(f"Utilisateur {utilisateur_a_supprimer} supprimé avec succès !")
        else:
            st.info("Aucun utilisateur disponible.")
    else:
        st.error("Accès refusé : Vous devez être administrateur pour gérer les utilisateurs.")

afficher_gestion_utilisateurs()