import streamlit as st
from database import get_db_connection
from datetime import datetime
# Charger le fichier CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Appliquer le CSS
load_css()
def determine_statut(date_debut, date_fin):
    today = datetime.today().date()
    if today < date_debut:
        return "À venir"
    elif date_debut <= today <= date_fin:
        return "En cours"
    else:
        return "Terminée"

def afficher_creer_mission():
        st.header("Créer une Nouvelle Mission")
        
        # Formulaire de création de mission
        nom_mission = st.text_input("Nom de la Mission")
        responsable = st.text_input("Responsable")
        date_debut = st.date_input("Date de Début")
        date_fin = st.date_input("Date de Fin")
        objectif = st.text_area("Objectif de la Mission")
        lieu = st.text_input("Lieu de la Mission")
        membres_equipe = st.multiselect("Membres de l'Équipe", ["Khadim DIOP", "Waly SENE", "Gilberta MANGA", "Aby K Diallo"])
        
        if st.button("Créer la Mission"):
            if nom_mission and responsable and objectif:
                # Déterminer le statut automatiquement
                statut = determine_statut(date_debut, date_fin)
                
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO missions (nom, responsable, date_debut, date_fin, objectif, statut, lieu, membres_equipe)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (nom_mission, responsable, date_debut, date_fin, objectif, statut, lieu, membres_equipe))
                conn.commit()
                conn.close()
                st.success("Mission créée avec succès !")
            else:
                st.error("Veuillez remplir tous les champs obligatoires : Nom de la Mission, Responsable et Objectif.")
 

afficher_creer_mission()