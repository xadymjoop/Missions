import streamlit as st
from database import get_db_connection

# Charger le fichier CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Appliquer le CSS
load_css()

def afficher_details_mission():
    st.header("Détails de la Mission")
    
    # Récupérer les missions depuis la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM missions')
    missions = cursor.fetchall()
    conn.close()
    
    # Sélection de la mission
    mission_selectionnee = st.selectbox("Choisir une mission", [mission[1] for mission in missions])
    
    if mission_selectionnee:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM missions WHERE nom = %s', (mission_selectionnee,))
        mission = cursor.fetchone()
        conn.close()
        
        st.subheader(f"Détails de {mission[1]}")
        
        # Affichage sous forme de tableau
        st.markdown(
            f"""
            <table class='mission-table'>
                <tr><th>Responsable</th><td>{mission[2]}</td></tr>
                <tr><th>Date de Début</th><td>{mission[3]}</td></tr>
                <tr><th>Date de Fin</th><td>{mission[4]}</td></tr>
                <tr><th>Objectif</th><td>{mission[5]}</td></tr>
                <tr><th>Statut</th><td>{mission[6]}</td></tr>
                <tr><th>Lieu</th><td>{mission[7]}</td></tr>
                <tr><th>Membres de l'Équipe</th><td>{', '.join(mission[8])}</td></tr>
            </table>
            """,
            unsafe_allow_html=True
        )

afficher_details_mission()
