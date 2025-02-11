import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import psycopg2
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os


st.set_page_config(page_title="Projet Sami et Tom", page_icon="⚽", layout="wide")

class Dashboard:
    def __init__(self):
        self.conn = None
        self.players = None
        self.setup_page()
        
        # Vérifier si les données sont déjà en session
        if "players_data" not in st.session_state:
            self.run_spider_and_load_data()
        else:
            self.players = st.session_state["players_data"]

        if self.players is not None:
            self.create_sidebar()
            section = st.sidebar.radio(
                "",
                ["Les Tops", "Les clubs", "Les joueurs", "Les corrélations"]
            )
            if section == "Les Tops" :
                self.diagramme1()
                self.diagramme2()
                self.diagramme3()
                self.diagramme4()
            elif section == "Les clubs" :
                self.diagramme5()
                self.diagramme6()
                self.diagramme7()
                self.diagramme8()
            elif section == "Les joueurs" :
                self.diagramme9()
                self.diagramme10()
                self.diagramme11()
                self.diagramme12()
                self.diagramme13()
                self.diagramme14()
                self.diagramme15()
                self.diagramme16()
            elif section == "Les corrélations" :
                self.diagramme17()
                self.diagramme18()
                self.diagramme19()
                self.diagramme20()

    def setup_page(self):
        st.title("Les statistiques des joueurs de Ligue 1")

    def create_sidebar(self):
        """Crée le menu latéral de navigation."""
        st.sidebar.title("Menu")

    def run_spider(self):
        """Lance le scraper Scrapy"""
        st.info("Lancement de la récupération des données avec Scrapy...")
        process = subprocess.Popen(['scrapy', 'crawl', 'ligue1_spider'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            st.success("Les données ont été récupérées avec succès.")
            return True
        else:
            st.error("Erreur lors de l'exécution de la spider.")
            st.error(stderr.decode("utf-8"))
            return False

    def connect_to_db(self):
        """Établit une connexion à la base PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "stats_ligue1"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "!2003BALLEROy"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432")
            )
        except Exception as e:
            st.error(f"Erreur de connexion à la base de données : {e}")
            return False
        return True

    def load_data_from_db(self):
        query = "SELECT * FROM joueurs;"
        try:
            self.players = pd.read_sql_query(query, self.conn)
            st.session_state["players_data"] = self.players  
            st.success("Les données ont été chargées avec succès depuis la base de données.")
        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")
            self.players = None

    def run_spider_and_load_data(self):
        """Lance le spider et charge les données depuis la base de données"""
        if not self.run_spider():
            return

        if self.connect_to_db():
            self.load_data_from_db()

    def diagramme1(self):
        st.header("I. Les Tops")
        st.subheader("1. Top 10 des meilleurs buteurs de Ligue 1 (toute competitions confondues)")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        top_10_buts_df = (self.players[['club', 'poste', 'nom', 'age', 'matchs_joués', 'buts']]
                      .sort_values(by="buts", ascending=False)
                      .head(10)
                      .reset_index(drop=True))

        top_10_buts_df = top_10_buts_df.rename(columns={
            'club': 'Club',
            'poste': 'Poste',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'buts': 'Buts'
        })

        top_10_buts_df.index = top_10_buts_df.index + 1

        st.table(top_10_buts_df)
    
    def diagramme2(self):
        st.subheader("2. Top 10 des meilleurs passeurs décisifs de Ligue 1")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        top_10_passes_df = (self.players[['club', 'poste', 'nom', 'age', 'matchs_joués', 'passes_d']]
                        .sort_values(by="passes_d", ascending=False)
                        .head(10)
                        .reset_index(drop=True))

        top_10_passes_df = top_10_passes_df.rename(columns={
            'club': 'Club',
            'poste': 'Poste',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'passes_d': 'Passes décisives'
        })

        top_10_passes_df.index = top_10_passes_df.index + 1

        st.table(top_10_passes_df)        

    def diagramme3(self):
        st.subheader("3. Top 10 des joueurs ayant le plus de buts + passes décisives")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return
        
        self.players['buts_plus_passes'] = self.players['buts'] + self.players['passes_d']        

        top_10_b_p_df = (self.players[['club', 'poste', 'nom', 'age', 'matchs_joués', 'buts', 'passes_d', 'buts_plus_passes']]
                        .sort_values(by="buts_plus_passes", ascending=False)
                        .head(10)
                        .reset_index(drop=True))

        top_10_b_p_df = top_10_b_p_df.rename(columns={
            'club': 'Club',
            'poste': 'Poste',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'buts': 'Buts',
            'passes_d': 'Passes décisives',
            'buts_plus_passes': 'Total buts + passes'
        })

        top_10_b_p_df.index = top_10_b_p_df.index + 1

        st.table(top_10_b_p_df) 

    def diagramme4(self):
        st.subheader("4. Top 10 des joueurs les plus jeunes de Ligue 1 ayant joué au moins 1 match")
    
        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        joueurs_actifs = (self.players[self.players['matchs_joués'] > 0]
                        .assign(age_num=self.players['age'].str.replace(" ans", "", regex=False).astype(int))
                        .sort_values(by="age_num", ascending=True)
                        .head(10)
                        .reset_index(drop=True))

        if joueurs_actifs.empty:
            st.warning("Aucun joueur n'a encore joué de match.")
            return
        
        top_10_jeunes_df = joueurs_actifs[['club', 'nom', 'age', 'matchs_joués']].rename(columns={
            'club': 'Club',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués'
        })

        top_10_jeunes_df.index = top_10_jeunes_df.index + 1

        st.table(top_10_jeunes_df)
    
    def diagramme5(self): 
        st.header("II. Les clubs")

        st.subheader("5. Classement des clubs par buts marqués")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        club_buts_df = self.players.groupby('club', as_index=False)['buts'].sum()

        club_buts_df['Club_Normalized'] = club_buts_df['club'].str.replace(" ", "").str.lower()

        club_buts_df = club_buts_df.sort_values(by="club", ascending=False)

        club_buts_df = club_buts_df.rename(columns={
            'club': 'Club',
            'buts': 'Total Buts'
        })

        couleurs_clubs = {
            "paris": "#0051A0",
            "marseille": "#7AC5D4",
            "lyon": "#1D58D2",
            "monaco": "#FFFFFF",
            "lille": "#B61826",
            "rennes": "#F13A3A",
            "nice": "#C8102E",
            "lens": "#E10600",
            "nantes": "#FFB81C",
            "strasbourg": "#005BAC",
            "toulouse": "#6C4F97",
            "reims": "#D10000",
            "brest": "#9E1B32",
            "montpellier": "#003B5C",
            "saint-etienne": "#A8D08D",
            "angers": "#000000",
            "lehavre": "#3C8B9C",
            "auxerre": "#FFFFFF"
        }

        club_buts_df["Couleur"] = club_buts_df["Club_Normalized"].map(couleurs_clubs).fillna("#CCCCCC")
    
        chart = alt.Chart(club_buts_df).mark_bar(stroke="#000000", strokeWidth=1).encode(
            x=alt.X("Total Buts:Q", scale=alt.Scale(domain=[0, club_buts_df["Total Buts"].max()])), 
            y=alt.Y("Club:N", sort="-x", axis=alt.Axis(labelLimit=250)), 
            color=alt.Color("Club_Normalized:N", scale=alt.Scale(domain=list(couleurs_clubs.keys()), range=list(couleurs_clubs.values()))),   
            tooltip=["Club", "Total Buts"] 
        ).properties(width=900, height=600).configure_legend(disable=True) 

        st.altair_chart(chart, use_container_width=True)

    def diagramme6(self):
        st.subheader("6. Top 5 des meilleurs buteurs et des meilleurs passeurs d'un club")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        club_selectionne = st.selectbox("Sélectionnez un club :", self.players['club'].unique())

        top_5_joueurs = (self.players[self.players['club'] == club_selectionne]
                         .assign(buts_plus_passes=lambda x: x['buts'] + x['passes_d'])
                         .sort_values(by="buts_plus_passes", ascending=False)
                         .head(5)
                         .rename(columns={
                            'poste': 'Poste', 'nom': 'Nom du joueur', 'age': 'Âge',
                            'matchs_joués': 'Matches joués', 'buts': 'Buts', 'passes_d': 'Passes décisives',
                            'buts_plus_passes': 'Total buts + passes'
                         })[['Poste', 'Nom du joueur', 'Âge', 'Matches joués', 'Buts', 'Passes décisives', 'Total buts + passes']]
                         .reset_index(drop=True))

        top_5_joueurs.insert(0, 'Rank', top_5_joueurs.index + 1)

        st.table(top_5_joueurs.set_index('Rank'))

    def diagramme7(self): 
        st.subheader("7. La part des buts + passes décisives par joueur pour un club")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        club_selectionne = st.selectbox("Choisissez un club", self.players['club'].unique())

        players_club = self.players[self.players['club'] == club_selectionne].copy()
        players_club['buts_plus_passes'] = players_club['buts'] + players_club['passes_d']

        top_players = players_club.sort_values(by="buts_plus_passes", ascending=False)

        pie_chart = px.pie(
            top_players, names='nom', values='buts_plus_passes', 
            width=800, height=600, labels={"nom": "Nom du joueur"}
        )

        pie_chart.update_traces(
            textinfo='percent', textposition='inside',
            marker=dict(line=dict(color="black", width=2)),
            customdata=top_players[['matchs_joués', 'buts', 'passes_d', 'buts_plus_passes']],
            hovertemplate="<b>%{label}</b><br>" +
                          "Matches joués: %{customdata[0]}<br>" +
                          "Buts: %{customdata[1]}<br>" +
                          "Passes décisives: %{customdata[2]}<br>" +
                          "Total buts + passes: %{customdata[3]}<br>"
        )

        pie_chart.update_layout(showlegend=False)

        st.plotly_chart(pie_chart)

    def diagramme8(self):
        st.subheader("8. Top 5 des joueurs les plus jeunes dans un club")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        club_selectionne = st.selectbox("Choisissez un club", self.players['club'].unique(), key="select_club_jeunes")
        joueurs_club = self.players[(self.players['club'] == club_selectionne) & (self.players['matchs_joués'] > 0)]

        if joueurs_club.empty:
            st.warning(f"Aucun joueur du club {club_selectionne} n'a encore joué de match.")
            return

        joueurs_club['age_num'] = joueurs_club['age'].str.replace(" ans", "", regex=False).astype(int)

        top_5_jeunes_df = joueurs_club.sort_values(by="age_num").head(5)[['poste', 'nom', 'age', 'matchs_joués', 'buts', 'passes_d']]

        top_5_jeunes_df = top_5_jeunes_df.rename(columns={
            'poste': 'Poste', 'nom': 'Nom du joueur', 'age': 'Âge', 'matchs_joués': 'Matches joués', 
            'buts': 'Buts', 'passes_d': 'Passes décisives'
        }).reset_index(drop=True)

        top_5_jeunes_df.index = top_5_jeunes_df.index + 1

        st.table(top_5_jeunes_df)

    def diagramme9(self):
        st.header("III. Les joueurs")
        st.subheader("9. Comparaison de deux joueurs")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        col1, col2 = st.columns(2)
        with col1:
            joueur_1 = st.selectbox("Sélectionnez le joueur 1 (Gauche) :", self.players["nom"].unique(), key="joueur_gauche")
        with col2:
            joueur_2 = st.selectbox("Sélectionnez le joueur 2 (Droite) :", self.players["nom"].unique(), key="joueur_droite")

        if not joueur_1 or not joueur_2:
            return

        data_j1 = self.players[self.players["nom"] == joueur_1].iloc[0]
        data_j2 = self.players[self.players["nom"] == joueur_2].iloc[0]

        def get_stats_labels(poste):
            stats_map = {
                "gardien": ("Arrêts", "Penaltys arrêtés"),
                "défenseur": ("Tacles", "Interceptions"),
                "milieu": ("Passes", "Tirs"),
                "attaquant": ("Tirs", "Dribbles réussis")
            }
            return stats_map.get(poste.strip().lower(), ("Stat_1", "Stat_2"))

        stat_1_j1, stat_2_j1 = get_stats_labels(data_j1["poste"])
        stat_1_j2, stat_2_j2 = get_stats_labels(data_j2["poste"])

        stats_keys = ["club", "poste", "numero", "age", "matchs_joués", "buts", "passes_d", "stat_1", "stat_2"]

        stats_labels_j1 = ["Club", "Poste", "Numéro", "Âge", "Matchs joués", "Buts", "Passes décisives", stat_1_j1, stat_2_j1]
        stats_labels_j2 = ["Club", "Poste", "Numéro", "Âge", "Matchs joués", "Buts", "Passes décisives", stat_1_j2, stat_2_j2]

        stats_j1 = [data_j1[k] for k in stats_keys]
        stats_j2 = [data_j2[k] for k in stats_keys]

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"### {joueur_1}")
            st.table(pd.DataFrame({"": stats_labels_j1, "Statistiques": stats_j1}).set_index(""))

        with col2:
            st.write(f"### {joueur_2}")
            st.table(pd.DataFrame({"": stats_labels_j2, "Statistiques": stats_j2}).set_index(""))

    def diagramme10(self):
        st.subheader("10. Top 5 des joueurs ayant le plus de matchs joués par poste")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        poste_selectionné = st.selectbox("Choisissez un poste", self.players['poste'].str.strip().str.lower().unique())

        top_joueurs = (self.players[self.players['poste'].str.strip().str.lower() == poste_selectionné]
                       .nlargest(5, 'matchs_joués')[['club', 'poste', 'nom', 'age', 'matchs_joués']]
                       .rename(columns={'club': 'Club', 'poste': 'Poste', 'nom': 'Nom du joueur', 
                                        'age': 'Âge', 'matchs_joués': 'Matches joués'})
                       .reset_index(drop=True))

        top_joueurs.index = top_joueurs.index + 1

        st.table(top_joueurs)

    def diagramme11(self):
        st.subheader("11. Répartition des âges par poste") 

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        self.players['age_num'] = self.players['age'].str.replace(" ans", "", regex=False).astype(int)

        clubs_disponibles = self.players['club'].unique()
        club_selectionne = st.selectbox("Choisissez un club", clubs_disponibles, key="select_club_jeunes2")

        joueurs_club = self.players[(self.players['club'] == club_selectionne) & (self.players['matchs_joués'] > 0)]

        if joueurs_club.empty:
            st.warning(f"Aucun joueur du club {club_selectionne} n'a encore joué de match.")
            return

        plt.figure(figsize=(10, 6))
        sns.violinplot(data=joueurs_club, x='poste', y='age_num', inner='quart', palette='muted')

        # Ajouter des titres et labels
        plt.title(f"Répartition des âges par poste pour le club {club_selectionne}", fontsize=16)
        plt.xlabel('Poste', fontsize=14)
        plt.ylabel('Âge', fontsize=14)

        st.pyplot(plt)

    def diagramme12(self):
        st.subheader("12. Top 10 des gardiens qui font le plus d'arrets")
        
        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        gardiens = self.players[self.players['poste'].str.replace(" ", "").str.lower() == "gardien"]

        top_10_arrets = gardiens.sort_values(by="stat_2", ascending=False).head(10)

        columns = ['club', 'nom', 'age', 'matchs_joués', 'stat_2']
        top_10_arrets_df = top_10_arrets[columns]
        top_10_arrets_df = top_10_arrets_df.reset_index(drop=False)
        top_10_arrets_df.index = top_10_arrets_df.index + 1
        top_10_arrets_df.drop('index', axis=1, inplace=True)

        top_10_arrets_df = top_10_arrets_df.rename(columns={
            'club': 'Club',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'stat_2': 'Intercepetions'
        })

        st.table(top_10_arrets_df)

    def diagramme13(self):
        st.subheader("13. Top 10 des defenseurs qui font le plus d'interceptions")
        
        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        defenseurs = self.players[self.players['poste'].str.replace(" ", "").str.lower() == "défenseur"]

        top_10_intercep = defenseurs.sort_values(by="stat_2", ascending=False).head(10)

        columns = ['club', 'nom', 'age', 'matchs_joués', 'stat_2']
        top_10_intercep_df = top_10_intercep[columns]
        top_10_intercep_df = top_10_intercep_df.reset_index(drop=False)
        top_10_intercep_df.index = top_10_intercep_df.index + 1
        top_10_intercep_df.drop('index', axis=1, inplace=True)

        top_10_intercep_df = top_10_intercep_df.rename(columns={
            'club': 'Club',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'stat_2': 'Intercepetions'
        })

        st.table(top_10_intercep_df)

    def diagramme14(self):
        st.subheader("14. Top 10 des milieux qui font le plus de passes")
        
        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        milieux = self.players[self.players['poste'].str.replace(" ", "").str.lower() == "milieu"]

        top_10_passes = milieux.sort_values(by="stat_1", ascending=False).head(10)

        columns = ['club', 'nom', 'age', 'matchs_joués', 'stat_1']
        top_10_passes_df = top_10_passes[columns]
        top_10_passes_df = top_10_passes_df.reset_index(drop=False)
        top_10_passes_df.index = top_10_passes_df.index + 1
        top_10_passes_df.drop('index', axis=1, inplace=True)

        top_10_passes_df = top_10_passes_df.rename(columns={
            'club': 'Club',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'stat_1': 'Passes'
        })

        st.table(top_10_passes_df)

    def diagramme15(self):
        st.subheader("15. Top 10 des attaquants qui font le plus de dribbles")
    
        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        attaquants = self.players[self.players['poste'].str.replace(" ", "").str.lower() == "attaquant"]

        top_10_dribbles = attaquants.sort_values(by="stat_2", ascending=False).head(10)

        columns = ['club', 'nom', 'age', 'matchs_joués', 'stat_2']
        top_10_dribbles_df = top_10_dribbles[columns]
        top_10_dribbles_df = top_10_dribbles_df.reset_index(drop=False)
        top_10_dribbles_df.index = top_10_dribbles_df.index + 1
        top_10_dribbles_df.drop('index', axis=1, inplace=True)

        top_10_dribbles_df = top_10_dribbles_df.rename(columns={
            'club': 'Club',
            'nom': 'Nom du joueur',
            'age': 'Âge',
            'matchs_joués': 'Matches joués',
            'stat_2': 'Dribbles'
        })

        st.table(top_10_dribbles_df)

    def diagramme16(self):
        st.subheader("16. Distribution des statistiques par poste") 

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        clubs_disponibles = self.players['club'].unique()
        club_selectionne = st.selectbox("Choisissez un club", clubs_disponibles, key="select_club_statistiques")

        joueurs_club = self.players[(self.players['club'] == club_selectionne) & (self.players['matchs_joués'] > 0)]

        if joueurs_club.empty:
            st.warning(f"Aucun joueur du club {club_selectionne} n'a encore joué de match.")
            return

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        sns.violinplot(data=joueurs_club, x='poste', y='buts', inner='quart', palette='muted', ax=axes[0])
        axes[0].set_title("Distribution des buts par poste", fontsize=14)
        axes[0].set_xlabel('Poste', fontsize=12)
        axes[0].set_ylabel('Buts', fontsize=12)

        sns.violinplot(data=joueurs_club, x='poste', y='passes_d', inner='quart', palette='muted', ax=axes[1])
        axes[1].set_title("Distribution des passes décisives par poste", fontsize=14)
        axes[1].set_xlabel('Poste', fontsize=12)
        axes[1].set_ylabel('Passes décisives', fontsize=12)

        sns.violinplot(data=joueurs_club, x='poste', y='matchs_joués', inner='quart', palette='muted', ax=axes[2])
        axes[2].set_title("Distribution des matchs joués par poste", fontsize=14)
        axes[2].set_xlabel('Poste', fontsize=12)
        axes[2].set_ylabel('Matchs joués', fontsize=12)

        plt.tight_layout()

        st.pyplot(fig)

    def diagramme17(self):
        st.header("IV. Les corrélations")

        st.subheader("17. Corrélation entre l'âge et la performance")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        self.players['age_num'] = self.players['age'].str.replace(" ans", "", regex=False).astype(int)

        joueurs_ayant_joue = self.players[self.players['matchs_joués'] > 0]

        if joueurs_ayant_joue.empty:
            st.warning("Aucun joueur n'a encore joué de match.")
            return

        fig, axes = plt.subplots(1, 1, figsize=(8, 6)) 

        sns.regplot(data=joueurs_ayant_joue, x='age_num', y='buts', scatter=False, line_kws={"color": "blue"}, ax=axes)
        axes.set_title("Âge vs Buts", fontsize=14)
        axes.set_xlabel('Âge', fontsize=12)
        axes.set_ylabel('Buts', fontsize=12)

        plt.tight_layout()

        col1, col2 = st.columns([3, 2])
        col3, col4 = st.columns([3, 2])

        col1.pyplot(fig)

        col2.markdown("""
        <div style="text-align: center;">
        **Graphique des Buts**<br>
        Ce graphique montre la relation entre l'âge des joueurs et leur nombre de buts marqués.  
        Ici, la ligne bleu montre la tendance générale entre l'age et le nombre de buts marqués. La zone d'ombre autour de la ligne montre la marge de variabilité des données.  
        On remarque donc qu'il n'y a pas de lien fort en l'age et le nombre de buts marqués. Les joueurs marquent en moyenne un nombre de buts similaire, quel que soit leur age.
        </div>
        """, unsafe_allow_html=True)

        col3.markdown("""
        <div style="text-align: center;">
        **Graphique des Passes Décisives**<br>
        Ce graphique montre la relation entre l'âge des joueurs et leur nombre de passes décisives.  
        Ici, la ligne verte montre la tendance générale entre l'age et le nombre de passes décisives. La zone d'ombre autour de la ligne montre la marge de variabilité des données.  
        On remarque donc qu'il y a un lien fort en l'age et le nombre de passes décisives. Cela montre que les joueurs plus agés tendent à réaliser plus de passes décisives en moyenne.
        </div>
        """, unsafe_allow_html=True)

        fig2, axes2 = plt.subplots(1, 1, figsize=(8, 6)) 

        sns.regplot(data=joueurs_ayant_joue, x='age_num', y='passes_d', scatter=False, line_kws={"color": "green"}, ax=axes2)
        axes2.set_title("Âge vs Passes Décisives", fontsize=14)
        axes2.set_xlabel('Âge', fontsize=12)
        axes2.set_ylabel('Passes Décisives', fontsize=12)

        plt.tight_layout()
        col4.pyplot(fig2)

    def diagramme18(self):
        st.subheader("18. Corrélation entre les tirs et les buts pour les attaquants")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        self.players['poste_normalise'] = self.players['poste'].str.lower().str.replace(" ", "")

        attaquants = self.players[self.players['poste_normalise'] == 'attaquant']

        if attaquants.empty:
            st.warning("Aucun attaquant trouvé.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))

        sns.regplot(data=attaquants, x='stat_1', y='buts', scatter=False, line_kws={"color": "red"}, ax=ax)
        ax.set_title("Corrélation entre les tirs et les buts des attaquants", fontsize=14)
        ax.set_xlabel('Tirs', fontsize=12)
        ax.set_ylabel('Buts', fontsize=12)

        plt.tight_layout()
        st.pyplot(fig)

    def diagramme19(self):
        st.subheader("19. Corrélation entre les tirs et les buts pour les milieux")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        self.players['poste_normalise'] = self.players['poste'].str.lower().str.replace(" ", "")

        milieux = self.players[self.players['poste_normalise'] == 'milieu']

        if milieux.empty:
            st.warning("Aucun milieu trouvé.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))

        sns.regplot(data=milieux, x='stat_2', y='buts', scatter=False, line_kws={"color": "green"}, ax=ax)
        ax.set_title("Corrélation entre les tirs et les buts des milieux", fontsize=14)
        ax.set_xlabel('Tirs', fontsize=12)
        ax.set_ylabel('Buts', fontsize=12)

        plt.tight_layout()
        st.pyplot(fig)

    def diagramme20(self):
        st.subheader("20. Corrélation entre les passes et les passes décisives pour les milieux")

        if self.players is None or self.players.empty:
            st.warning("Aucune donnée disponible. Veuillez vérifier la récupération des données.")
            return

        self.players['poste_normalise'] = self.players['poste'].str.lower().str.replace(" ", "")

        milieux = self.players[self.players['poste_normalise'] == 'milieu']

        if milieux.empty:
            st.warning("Aucun milieu trouvé.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))

        sns.regplot(data=milieux, x='stat_1', y='passes_d', scatter=False, line_kws={"color": "blue"}, ax=ax)
        ax.set_title("Corrélation entre les passes et les passes décisives des milieux", fontsize=14)
        ax.set_xlabel('Passes', fontsize=12)
        ax.set_ylabel('Passes décisives', fontsize=12)

        plt.tight_layout()
        st.pyplot(fig)

if __name__ == "__main__":
    Dashboard()