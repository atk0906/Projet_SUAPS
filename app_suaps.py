import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import ssl
from streamlit_extras.app_logo import add_logo

# Định nghĩa theme color palette cho toàn bộ dashboard
COLORS = {
    "primary": "#1E88E5",      
    "secondary": "#26A69A",    
    "accent": "#FF8A65",       
    "neutral": "#78909C",     
    "background": "#F5F7FA",   
    "text": "#37474F",          
}

# Color sequences cho các biểu đồ
COLOR_SEQUENCE = [COLORS["primary"], COLORS["secondary"], COLORS["accent"], 
                  "#7986CB", "#4DB6AC", "#FFB74D", "#BA68C8", "#4FC3F7"]

# Color scales cho heatmap và continuous colors
COLOR_SCALE = ["#E3F2FD", "#90CAF9", "#42A5F5", "#1E88E5", "#1565C0"]

def setting_web_attribute(page_title):
    """Set basic web attribute.

    Args:
        page_title: Title of the page.
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    st.set_page_config(page_title=page_title, layout="wide")
    st.markdown(
        f"""
            <style>
                html {{
                    zoom: 80%;}}
                .block-container {{
                    padding-top: 1rem;
                    margin-top: 0rem; 
                    padding-bottom: 1rem;
                    padding-left: 3rem;
                    padding-right: 3rem;
                }}
                .metric-container {{
                    font-size: 70px !important;
                    font-weight: bold;
                    margin-top: 0.5rem;
                    color: {COLORS["primary"]};
                }}
                h1, h2, h3, h4 {{
                    color: {COLORS["text"]};
                }}
                .stTabs [data-baseweb="tab-list"] {{
                    gap: 10px;
                }}
                .stTabs [data-baseweb="tab"] {{
                    height: 50px;
                    white-space: pre-wrap;
                    background-color: {COLORS["background"]};
                    border-radius: 4px 4px 0px 0px;
                    gap: 1px;
                    padding-top: 10px;
                    padding-bottom: 10px;
                }}
                .stTabs [aria-selected="true"] {{
                    background-color: {COLORS["primary"]};
                    color: white;
                }}
                div[data-testid="stSidebarNav"] li div a {{
                    margin-left: 1rem;
                    padding: 1rem;
                    width: 300px;
                    border-radius: 0.5rem;
                }}
                div[data-testid="stSidebarNav"] li div::focus-visible {{
                    background-color: rgba(151, 166, 195, 0.15);
                }}
                div[data-testid="stSidebarNav"] li div a:hover {{
                    background-color: {COLORS["background"]};
                }}
                div[data-testid="stSidebarNav"] li div::before {{
                    content: '✦';
                    color: {COLORS["primary"]};
                    margin-right: 0.5rem;
                }}
                div.stButton > button:first-child {{
                    background-color: {COLORS["primary"]};
                    color: white;
                    border: none;
                }}
                div.stButton > button:hover {{
                    background-color: {COLORS["secondary"]};
                    color: white;
                    border: none;
                }}
                .reportview-container .main .block-container {{
                    background-color: {COLORS["background"]};
                }}
                .card {{
                    background-color: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                }}
                .small-text {{
                    font-size: 12px;
                    color: {COLORS["neutral"]};
                }}
                .stat-title {{
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: {COLORS["text"]};
                }}
                .stSelectbox label, .stRadio label {{
                    color: {COLORS["text"]};
                    font-weight: bold;
                }}
            </style>
            """,
        unsafe_allow_html=True,
    )

def card_container(title, content):
    """Helper to create a card container with uniform styling"""
    st.markdown(f"""
    <div class="card">
        <div class="stat-title">{title}</div>
        {content}
    </div>
    """, unsafe_allow_html=True)

def V_SPACE(lines):
    """Blank lines for spacing purposes."""
    for _ in range(lines):
        st.write("&nbsp;")
        
def VB_SPACE(lines):
    """Blank lines for spacing purposes sidebar."""
    for _ in range(lines):
        st.sidebar.write("&nbsp;")

# Initialiser les paramètres de la page
setting_web_attribute("Analyse du Service des Sports")

# Sidebar avec un design amélioré
st.sidebar.image("assert/logo-ubs.png", use_container_width=False, width=120)
st.sidebar.title("Tableau de Bord")


# Sidebar pour sélectionner le semestre ou l'événement
st.sidebar.header("Sélectionnez le semestre")
option = st.sidebar.radio(
    "Choisissez une option :", ["Semestre 1", "Semestre 2", "Événements"]
)

# Chargement des données en fonction du choix
if option == "Semestre 1":
    DATA_PATH = "data/fixed_ses1.csv"
elif option == "Semestre 2":
    DATA_PATH = "data/fixed_ses2.csv"
else:
    DATA_PATH = "data/fixed_even.csv"

# Load data
df = pd.read_csv(DATA_PATH)
# Load presence data (BASKET - LORIENT)
df_confirme = pd.read_csv("data/presence_basket_confirme.csv")
df_debutant = pd.read_csv("data/presence_basket_debutant.csv")

# Site selection with improved styling
VB_SPACE(1)
selected_site = st.sidebar.selectbox("Sélectionnez le site :", ["Tous", "VANNES", "LORIENT"], index=0)

if "Site" in df.columns and selected_site != "Tous":
    df = df[df["Site"] == selected_site]

# Header with banner style
st.markdown(f"""
<div style='background-color: {COLORS["primary"]}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
    <h1 style='color: white; text-align: center;'>Analyse du Service des Sports</h1>
    <p style='color: white; text-align: center; font-style: italic;'>
        {option} {f'- {selected_site}' if selected_site != 'Tous' else '- Tous les sites'}
    </p>
</div>
""", unsafe_allow_html=True)

# Tab structure with improved styling
tab1, tab2, tab3, tab5, tab4 = st.tabs(["📊 Vue d'ensemble", "📈 Statistiques Principales", 
                                       "🔍 Analyse Avancée", "🏀 Présence BASKET - LORIENT", 
                                       "👥 Analyse des Étudiants"])

with tab1:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: #1E88E5; margin-top: 0;'>Nombre Total d'Étudiants</h3>
        """, unsafe_allow_html=True)
        
        if "Prénom" in df.columns and "Nom de famille" in df.columns:
            total_students = df.drop_duplicates(subset=["Prénom", "Nom de famille"]).shape[0]
        else:
            total_students = df.shape[0]
        st.markdown(f"<div class='metric-container'>{total_students}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #1E88E5; margin-top: 0;'>Répartition par Groupement d'activités</h3>
        """, unsafe_allow_html=True)
        
        if "Groupement d’activités" in df.columns:
            groupement_counts = df["Groupement d’activités"].value_counts().reset_index()
            groupement_counts.columns = ["Groupement d’activités", "Nombre d'étudiants"]
            fig_groupement = px.bar(
                groupement_counts, 
                x="Groupement d’activités", 
                y="Nombre d'étudiants",
                text_auto=True,
                color="Nombre d'étudiants",
                color_continuous_scale=COLOR_SCALE
            )
            fig_groupement.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS["text"]),
                margin=dict(l=0, r=0, t=10, b=40),  
                width=None,  
                height=400   
            )
            st.plotly_chart(fig_groupement, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


    with col2:
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: #1E88E5; margin-top: 0;'>Nombre d'Activités Sportives</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div class='metric-container'>{df['Activité'].nunique()}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #1E88E5; margin-top: 0;'>Répartition par Type d'inscription</h3>
        """, unsafe_allow_html=True)
        
        if "Type d’inscription" in df.columns:
            inscription_counts = df["Type d’inscription"].value_counts()
            fig_inscription = px.pie(
                values=inscription_counts.values,
                names=inscription_counts.index,
                color_discrete_sequence=COLOR_SEQUENCE,
                hole=0.4
            )
            fig_inscription.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS["text"]),
                margin=dict(l=20, r=20, t=10, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_inscription, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


    with col3:
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: #1E88E5; margin-top: 0;'>Nombre Total d'Enseignants</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div class='metric-container'>{df['Enseignant'].nunique()}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #1E88E5; margin-top: 0;'>Répartition par Type</h3>
        """, unsafe_allow_html=True)
        
        if "Type" in df.columns:
            df_unique = df.drop_duplicates(subset=["Prénom", "Nom de famille", "Type"])
            type_counts = df_unique["Type"].value_counts()
            fig_type = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                color_discrete_sequence=COLOR_SEQUENCE,
                hole=0.4
            )
            fig_type.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS["text"]),
                margin=dict(l=20, r=20, t=10, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_type, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    st.markdown(f"""
    <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
        <h2 style='color: {COLORS["primary"]}; margin-top: 0;'>Statistiques Principales</h2>
        <p style='color: {COLORS["text"]};'>Vue d'ensemble des statistiques clés du service des sports.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    # Top activités les plus populaires
    with col1:
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Top Activités les Plus Populaires</h3>
        """, unsafe_allow_html=True)
        
        top_activites = df["Activité"].value_counts().head(10).reset_index()
        top_activites.columns = ["Activité", "Nombre d'inscriptions"]
        fig = px.bar(
            top_activites, 
            x="Activité", 
            y="Nombre d'inscriptions", 
            text_auto=True,
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=80),
            xaxis=dict(tickangle=-45)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Répartition des inscriptions par département
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Répartition des Inscriptions par Département</h3>
        """, unsafe_allow_html=True)
        
        departments = df["Département"].value_counts().reset_index()
        departments.columns = ["Département", "Nombre d'inscriptions"]
        departments = departments.sort_values(by="Nombre d'inscriptions", ascending=True)
        fig = px.bar(
            departments, 
            y="Département", 
            x="Nombre d'inscriptions",
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE,
            text_auto=True
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Répartition des inscriptions par jour
    with col2:
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Répartition des Inscriptions par Jour</h3>
        """, unsafe_allow_html=True)

        
        inscriptions_par_jour = df["Jour"].value_counts().reset_index()
        inscriptions_par_jour.columns = ["Jour", "Nombre d'inscriptions"]
        fig = px.bar(
            inscriptions_par_jour, 
            x="Jour", 
            y="Nombre d'inscriptions", 
            text_auto=True,
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Répartition des inscriptions par site
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Répartition des Inscriptions par Site</h3>
        """, unsafe_allow_html=True)
        
        inscriptions_par_site = df["Site"].value_counts().reset_index()
        inscriptions_par_site.columns = ["Site", "Nombre d'inscriptions"]
        fig = px.bar(
            inscriptions_par_site, 
            x="Site", 
            y="Nombre d'inscriptions",
            text_auto=True,
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown(f"""
    <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
        <h2 style='color: {COLORS["primary"]}; margin-top: 0;'>Analyse Avancée</h2>
        <p style='color: {COLORS["text"]};'>Analyse détaillée des tendances et des statistiques avancées.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        # Distribution par Niveau
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Distribution des Inscriptions par Niveau</h3>
        """, unsafe_allow_html=True)
        
        niveau_dist = df["Niveau"].value_counts().reset_index()
        niveau_dist.columns = ["Niveau", "Nombre d'inscriptions"]
        fig = px.bar(
            niveau_dist, 
            x="Niveau", 
            y="Nombre d'inscriptions",
            text_auto=True,
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin_autoexpand=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Répartition par Horaires
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Répartition des Inscriptions par Horaires</h3>
        """, unsafe_allow_html=True)
        
        df["Période"] = pd.cut(pd.to_datetime(df["Horaires"].str[:5], format="%H:%M", errors='coerce').dt.hour,
                               bins=[0, 12, 18, 24],
                               labels=["Matin", "Après-midi", "Soir"],
                               right=False)
        horaires_dist = df["Période"].value_counts().reset_index()
        horaires_dist.columns = ["Période", "Nombre d'inscriptions"]
        fig = px.bar(
            horaires_dist, 
            x="Période", 
            y="Nombre d'inscriptions",
            text_auto=True,
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=40),
            xaxis=dict(categoryorder='array', categoryarray=['Matin', 'Après-midi', 'Soir'])
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Top Enseignants
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Top Enseignants les Plus Populaires</h3>
        """, unsafe_allow_html=True)
        
        top_enseignants = df["Enseignant"].value_counts().head(10).reset_index()
        top_enseignants.columns = ["Enseignant", "Nombre d'inscriptions"]
        fig = px.bar(
            top_enseignants, 
            x="Enseignant", 
            y="Nombre d'inscriptions",
            text_auto=True,
            color="Nombre d'inscriptions",
            color_continuous_scale=COLOR_SCALE
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=80),
            xaxis=dict(tickangle=-45)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Heatmap des Inscriptions par Jour et Heure
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Heatmap des Inscriptions par Jour et Heure</h3>
        """, unsafe_allow_html=True)
        
        heatmap_data = df.groupby(["Jour", "Horaires"]).size().reset_index(name="Nombre d'inscriptions")
        fig = px.density_heatmap(
            heatmap_data, 
            x="Jour", 
            y="Horaires", 
            z="Nombre d'inscriptions", 
            color_continuous_scale=COLOR_SCALE
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=40, r=40, t=10, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        
with tab5:
    st.markdown(f"""
    <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
        <h2 style='color: {COLORS["primary"]}; margin-top: 0;'>Présence des Étudiants - BASKET - LORIENT</h2>
        <p style='color: {COLORS["text"]};'>Analyse de la présence des étudiants aux cours de basket à Lorient.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Données de Présence</h3>
        """, unsafe_allow_html=True)

        # Choisir niveau (Débutant ou Confirmé)
        niveau_choice = st.selectbox("Sélectionnez le niveau :", ["Débutant", "Confirmé"], index=0)

        # Utiliser les données de présence
        if niveau_choice == "Débutant":
            df_basket = df_debutant[df_debutant["Activité"] == "BASKET - LORIENT"]
        else:
            df_basket = df_confirme[df_confirme["Activité"] == "BASKET - LORIENT"]

        # Traiter les noms des colonnes de cours
        original_cours_columns = [col for col in df_basket.columns if col.startswith("Cours n°")]
        renamed_cours_columns = {col: "Cours " + col.split(" ")[1] for col in original_cours_columns}

        # Renommer les colonnes
        df_basket.rename(columns=renamed_cours_columns, inplace=True)

        # Compter les présences (Présent ou En retard considérés comme Présent)
        presence_data = []
        total_students = len(df_basket)

        for col in renamed_cours_columns.values():
            if col in df_basket.columns:
                count_present = df_basket[col].isin(["Présent", "En retard"]).sum()
                taux_participation = (count_present / total_students) * 100
                presence_data.append([col, count_present, round(taux_participation, 2)])

        presence_df = pd.DataFrame(presence_data, columns=["Cours", "Nombre d'étudiants présents", "Taux de Participation (%)"])
        presence_df = presence_df.sort_values(by="Cours")

        # Styliser le tableau avec un thème cohérent
        st.dataframe(
            presence_df,
            column_config={
                "Cours": st.column_config.TextColumn("Cours"),
                "Nombre d'étudiants présents": st.column_config.NumberColumn(
                    "Nombre d'étudiants présents",
                    format="%d"
                ),
                "Taux de Participation (%)": st.column_config.ProgressColumn(
                    "Taux de Participation (%)",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                    help="Pourcentage des étudiants présents au cours"
                )
            },
            use_container_width=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sélection de cours avec style amélioré
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Détails par Cours</h3>
        """, unsafe_allow_html=True)
        
        # Choisir un cours pour voir les participants
        selected_cours = st.selectbox("Choisissez un cours pour voir les participants :", presence_df["Cours"].unique())

        if selected_cours:
            st.subheader(f"Participants au {selected_cours}")

            if selected_cours in df_basket.columns:
                # Filtrer les étudiants présents ou en retard
                participants = df_basket[df_basket[selected_cours].isin(["Présent", "En retard"])]

                # Afficher la liste des étudiants avec un statut
                if "Prénom" in participants.columns and "Nom de famille" in participants.columns:
                    participant_names = participants[["Prénom", "Nom de famille", "Adresse de courriel", "Sexe"]]
                    
                    # Ajouter une colonne de statut
                    participant_names["Statut"] = participants[selected_cours]
                    
                    # Appliquer un style cohérent aux données
                    st.dataframe(
                        participant_names,
                        column_config={
                            "Statut": st.column_config.TextColumn(
                                "Statut",
                                help="Statut de présence au cours",
                                width="medium"
                            ),
                            "Sexe": st.column_config.TextColumn(
                                "Sexe",
                                width="small"
                            )
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Afficher des statistiques sommaires
                    st.markdown(f"""
                    <div style='margin-top: 15px; padding: 10px; background-color: {COLORS["background"]}; border-radius: 5px;'>
                        <p><strong>Total de participants:</strong> {len(participant_names)}</p>
                        <p><strong>Répartition F/M:</strong> {participant_names['Sexe'].value_counts().to_dict()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.warning("Les colonnes 'Prénom' et 'Nom de famille' ne sont pas disponibles dans le fichier.")
            else:
                st.info("Aucun étudiant n'a participé à ce cours.")
        
        st.markdown("</div>", unsafe_allow_html=True)

    
    with col2:
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Répartition des Genres</h3>
        """, unsafe_allow_html=True)
        
        presence_df = presence_df.sort_values(by="Cours")
        df_basket["Sexe"] = df_basket["Sexe"].replace({"F": "Femme", "M": "Homme"})

        genre_counts = df_basket["Sexe"].value_counts().reset_index()
        genre_counts.columns = ["Sexe", "Nombre d'étudiants"]

        fig_pie = px.pie(
            genre_counts, 
            names="Sexe", 
            values="Nombre d'étudiants",
            title="Répartition des Genres",
            color_discrete_sequence=[COLORS["primary"], COLORS["accent"]],
            hole=0.4
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Graphique d'évolution de présence
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Évolution de la Présence</h3>
        """, unsafe_allow_html=True)
        
        # Graphique de ligne pour la présence (trié par cours)
        fig = px.line(
            presence_df, 
            x="Cours", 
            y="Nombre d'étudiants présents",
            title=f"Présence des Étudiants - BASKET - LORIENT ({niveau_choice})",
            markers=True,
            color_discrete_sequence=[COLORS["primary"]]
        )
        
        # Ajouter une ligne pour le taux de participation
        fig.add_trace(
            go.Scatter(
                x=presence_df["Cours"],
                y=presence_df["Taux de Participation (%)"],
                name="Taux de Participation (%)",
                yaxis="y2",
                line=dict(color=COLORS["accent"], width=2, dash="dot"),
                mode="lines+markers"
            )
        )
        
        # Configurer le deuxième axe y
        fig.update_layout(
            yaxis2=dict(
                title="Taux de Participation (%)",
                overlaying="y",
                side="right",
                range=[0, 100],
                ticksuffix="%"
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(l=40, r=60, t=50, b=60),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Ajouter un graphique de type jauge pour le taux de présence moyen
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Taux de Présence Moyen</h3>
        """, unsafe_allow_html=True)
        
        avg_presence_rate = presence_df["Taux de Participation (%)"].mean()
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_presence_rate,
            title={"text": f"Taux Moyen de Participation - {niveau_choice}"},
            gauge={
                "axis": {"range": [0, 100], "ticksuffix": "%"},
                "bar": {"color": COLORS["primary"]},
                "steps": [
                    {"range": [0, 50], "color": "#FFCDD2"},
                    {"range": [50, 75], "color": "#FFECB3"},
                    {"range": [75, 100], "color": "#C8E6C9"}
                ],
                "threshold": {
                    "line": {"color": COLORS["accent"], "width": 4},
                    "thickness": 0.75,
                    "value": avg_presence_rate
                }
            }
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=20, r=20, t=60, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        
with tab4:
    st.markdown(f"""
    <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
        <h2 style='color: {COLORS["primary"]}; margin-top: 0;'>Analyse des Étudiants - Département vs Activité</h2>
        <p style='color: {COLORS["text"]};'>Analyse croisée des inscriptions par département et activité.</p>
    </div>
    """, unsafe_allow_html=True)

    # Vérifier si les colonnes Département et Activité existent
    if "Département" in df.columns and "Activité" in df.columns:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
                <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Répartition des Étudiants</h3>
            """, unsafe_allow_html=True)
            
            # Calculer les effectifs par Département et Activité
            department_activity = df.groupby(["Département", "Activité"]).size().reset_index(name="Nombre d'étudiants")

            # Créer le scatter plot avec taille ajustée
            fig_scatter = px.scatter(
                department_activity,
                x="Département",
                y="Activité",
                size="Nombre d'étudiants",
                color="Département",
                hover_data=["Nombre d'étudiants"],
                color_discrete_sequence=COLOR_SEQUENCE,
                title="Répartition des Étudiants par Département et Activité"
            )
            
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS["text"]),
                margin=dict(l=40, r=40, t=50, b=80),
                height=600
            )

            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
                <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Top Départements</h3>
            """, unsafe_allow_html=True)
            
            dept_counts = df["Département"].value_counts().head(8)
            dept_df = pd.DataFrame({
                "Département": dept_counts.index,
                "Nombre d'inscriptions": dept_counts.values
            })
            dept_df = dept_df.sort_values(by="Nombre d'inscriptions", ascending=True)

            fig_dept = px.bar(
                dept_df,
                x="Nombre d'inscriptions",
                y="Département",
                orientation='h',
                color="Nombre d'inscriptions",
                color_continuous_scale=COLOR_SCALE,
                text_auto=True
            )
            
            fig_dept.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS["text"]),
                margin=dict(l=20, r=40, t=10, b=20),
                xaxis_title="Nombre d'étudiants",
                yaxis_title="Département",
                showlegend=False
            )
            
            st.plotly_chart(fig_dept, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Limiter aux top départements et activités pour une meilleure lisibilité
        st.markdown(f"""
        <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: {COLORS["primary"]}; margin-top: 0;'>Marimekko Plot - Top Départements & Activités</h3>
        """, unsafe_allow_html=True)
        
        top_departments = department_activity.groupby("Département")["Nombre d'étudiants"].sum().nlargest(10).index
        top_activities = department_activity.groupby("Activité")["Nombre d'étudiants"].sum().nlargest(10).index

        department_activity_filtered = department_activity[department_activity["Département"].isin(top_departments)]
        department_activity_filtered = department_activity_filtered[department_activity_filtered["Activité"].isin(top_activities)]

        # Créer le graphique Treemap (Marimekko)
        fig_mosaic = px.treemap(
            department_activity_filtered, 
            path=["Département", "Activité"], 
            values="Nombre d'étudiants",
            color="Nombre d'étudiants",
            color_continuous_scale="Blues",
            title="Distribution des Inscriptions - Top Départements et Activités"
        )

        fig_mosaic.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS["text"]),
            margin=dict(l=20, r=20, t=50, b=20),
            height=500
        )
        
        st.plotly_chart(fig_mosaic, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("Les colonnes 'Département' et 'Activité' ne sont pas disponibles dans les données.")

# Footer avec informations de copyright et version
st.markdown(f"""
<div style='background-color: {COLORS["primary"]}; padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center;'>
    <p style='color: white; margin: 0;'>© 2025 - Analyse du Service des Sports | Université Bretagne Sud</p>
</div>
""", unsafe_allow_html=True)
