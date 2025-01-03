import streamlit as st
import psycopg2
from database import get_db_connection

# Charger le fichier CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Appliquer le CSS
load_css()

def afficher_supprimer_mission():
    # Vérifier si l'utilisateur est connecté et a le rôle d'administrateur
    if st.session_state.get('role') != "Administrateur":
        st.error("Accès refusé : Vous devez être administrateur pour supprimer une mission.")
        return  # Arrêter l'exécution de la fonction si l'utilisateur n'est pas administrateur

    st.header("Supprimer une Mission")

    # Récupérer les missions depuis la base de données
    conn = get_db_connection()
    if conn is None:
        st.error("Impossible de se connecter à la base de données.")
        return  # Arrêter l'exécution si la connexion échoue

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM missions')
        missions = cursor.fetchall()

        if not missions:
            st.warning("Aucune mission trouvée dans la base de données.")
            return  # Aucune mission à supprimer

        # Sélection de la mission à supprimer
        mission_a_supprimer = st.selectbox(
            "Choisir une mission à supprimer",
            [mission[1] for mission in missions]  # Afficher les noms des missions
        )

        # Bouton pour supprimer la mission
        if st.button("Supprimer la Mission"):
            try:
                # Supprimer la mission sélectionnée
                cursor.execute('DELETE FROM missions WHERE nom = %s', (mission_a_supprimer,))
                conn.commit()
                st.success(f"Mission '{mission_a_supprimer}' supprimée avec succès !")
            except psycopg2.Error as e:
                st.error(f"Erreur lors de la suppression de la mission : {e}")
    except psycopg2.Error as e:
        st.error(f"Erreur lors de la récupération des missions : {e}")
    finally:
        # Fermer la connexion à la base de données
        if conn:
            conn.close()

# Afficher l'interface de suppression de mission
afficher_supprimer_mission()