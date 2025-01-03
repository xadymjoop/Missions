import streamlit as st
import pandas as pd
from database import get_db_connection
from datetime import datetime

# Charger le CSS en premier
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Charger FontAwesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)

# Titre de la page
st.title("Tableau de Bord")

# Charger le CSS en premier
st.markdown("""
    <style>
        div[data-testid="stSidebar"] .stSelectbox label {
            color: black !important;
        }
        div[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Charger FontAwesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)


# Récupérer les missions depuis la base de données
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT * FROM missions')
missions = cursor.fetchall()
conn.close()

# Calculer le nombre de missions en cours
if missions:
    df = pd.DataFrame(missions, columns=["ID", "Mission", "Responsable", "Date de Début", "Date de Fin", "Objectif", "Statut", "Lieu", "Membres de l'Équipe"])
    missions_en_cours = df[df["Statut"] == "En cours"].shape[0]
else:
    missions_en_cours = 0

# Afficher le nombre de missions en cours
st.markdown(f"""
    <div class="stMetric">
        <h3><i class="fas fa-tasks"></i> Missions en cours</h3>
        <p>{missions_en_cours}</p>
    </div>
""", unsafe_allow_html=True)

def determine_statut(date_debut, date_fin):
    today = datetime.today().date()
    if today < date_debut:
        return "À venir"
    elif date_debut <= today <= date_fin:
        return "En cours"
    else:
        return "Terminée"

def get_row_color(statut):
    if statut == "Terminée":
        return "background-color: rgba(255, 0, 0, 0.2);"
    elif statut == "En cours":
        return "background-color: rgba(0, 255, 0, 0.2);"
    elif statut == "À venir":
        return "background-color: rgba(0, 0, 255, 0.2);"
    return ""

def add_status_icons(statut):
    if statut == "Terminée":
        return "✅ Terminée"
    elif statut == "En cours":
        return "⏳ En cours"
    elif statut == "À venir":
        return "📅 À venir"
    return statut

def afficher_tableau_de_bord():
    if missions:
        # Convertir les résultats en DataFrame
        df = pd.DataFrame(missions, columns=["ID", "Nom", "Responsable", "Date de Début", "Date de Fin", "Objectif", "Statut", "Lieu", "Membres de l'Équipe"])
        
        # Supprimer la colonne ID
        df = df.drop(columns=["ID"])
        
        # Ajouter des icônes aux statuts
        df["Statut"] = df["Statut"].apply(add_status_icons)
        
        # Créer une colonne temporaire pour le filtrage (sans icônes)
        df["Statut_Filtre"] = df["Statut"].str.replace("✅ ", "").str.replace("⏳ ", "").str.replace("📅 ", "")
        
        # Filtre par statut
        filter_statut = st.sidebar.selectbox("Statut", ["Tous", "À venir", "En cours", "Terminée"])
        
        if filter_statut != "Tous":
            df = df[df["Statut_Filtre"] == filter_statut]
        
        # Supprimer la colonne temporaire après le filtrage
        df = df.drop(columns=["Statut_Filtre"])
        
        # Appliquer les couleurs aux lignes
        def color_rows(row):
            return [get_row_color(row["Statut"])] * len(row)
        
        # Appliquer la fonction de couleur aux lignes
        styled_df = df.style.apply(color_rows, axis=1)
        
        # Afficher le tableau stylisé
        st.dataframe(styled_df, use_container_width=True)
        
        # Bouton pour exporter les données au format CSV
        if st.button("Exporter les Missions en CSV"):
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name="missions.csv",
                mime="text/csv",
            )
    else:
        st.info("Aucune mission disponible.")

afficher_tableau_de_bord()