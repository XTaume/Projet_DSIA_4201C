import scrapy
import psycopg2
import os

class Ligue1Spider(scrapy.Spider):
    name = "ligue1_spider"
    start_urls = [
        'https://www.footmercato.net/club/angers-sco/effectif/',
        'https://www.footmercato.net/club/association-jeunesse-auxerroise/effectif/',
        'https://www.footmercato.net/club/stade-brestois-29/effectif/',
        'https://www.footmercato.net/club/hac/effectif/',
        'https://www.footmercato.net/club/racing-club-de-lens/effectif/',
        'https://www.footmercato.net/club/losc/effectif/',
        'https://www.footmercato.net/club/ol/effectif/',
        'https://www.footmercato.net/club/om/effectif/',
        'https://www.footmercato.net/club/as-monaco/effectif/',
        'https://www.footmercato.net/club/montpellier-hsc/effectif/',
        'https://www.footmercato.net/club/fc-nantes/effectif/',
        'https://www.footmercato.net/club/ogc-nice/effectif/',
        'https://www.footmercato.net/club/psg/effectif/',
        'https://www.footmercato.net/club/stade-de-reims/effectif/',
        'https://www.footmercato.net/club/stade-rennais-fc/effectif/',
        'https://www.footmercato.net/club/asse/effectif/',
        'https://www.footmercato.net/club/rc-strasbourg-alsace/effectif/',
        'https://www.footmercato.net/club/tfc/effectif/'
    ]

    def clear_table(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM joueurs;")
            conn.commit()
            self.logger.info("Table 'joueurs' vidée avec succès.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression des données : {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def start_requests(self):
        self.clear_table()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def connect_to_db(self):
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )

    
    def insert_player_data(self, player_data):
        """Insère les données d'un joueur dans la table joueurs"""
        conn = self.connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO joueurs (club, poste, numero, nom, age, matchs_joués, buts, passes_d, stat_1, stat_2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    player_data["club"],
                    player_data["poste"],
                    player_data["numero"],
                    player_data["nom"],
                    player_data["age"],
                    player_data["matchs_joués"],
                    player_data["buts"],
                    player_data["passes_d"],
                    player_data["stat_1"],
                    player_data["stat_2"]
                )
            )
            conn.commit()
        except Exception as e:
            self.logger.error(f"Erreur lors de l'insertion des données : {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def parse(self, response):
        club_name = response.css('div.pageDataHeaderIdentity__label::text').get()
        club_name = club_name.strip() if club_name else "Club inconnu"

        if club_name == "OM 2024/2025":
            club_name = "Marseille"
        if club_name == "PSG 2024/2025":
            club_name = "Paris"      
        if club_name == "ASSE":
            club_name = "Saint-Etienne"    

        raw_data = response.xpath('//div[@id="playerTables" and contains(@class, "wrapper")]//text()').getall()
        self.logger.info(f"Raw Data: {raw_data}")

        data = [line.strip() for line in raw_data if line.strip()]
    
        sections = []
        current_section = []
        temp_group = [] 
        temp_group_8 = []
        temp_group_size = 5 
        temp_group_8_size = 8
    
        section_titles = ["Gardiens", "Défenseurs", "Milieux", "Attaquants"]
        autre_title = ["Poste non défini"]

        cleaned_data = []
        for item in data :
            if item=="-" :
                cleaned_data.append(int(0))
            elif item.isdigit():
                cleaned_data.append(int(item))
            else:
                cleaned_data.append(item)

        for line in cleaned_data:
            if line in section_titles or line in autre_title:
                if current_section:
                    if temp_group:
                        current_section.insert(1, temp_group)
                    if temp_group_8:
                        current_section.extend(temp_group_8)
                    sections.append(current_section)

                current_section = [line]
                temp_group = []
                temp_group_8 = []

                if line in autre_title:
                    temp_group_size = 3
                    temp_group_8_size = 6
                else:
                    temp_group_size = 5
                    temp_group_8_size = 8
            else:
                if len(temp_group) < temp_group_size:
                    temp_group.append(line)
                elif len(temp_group_8) < temp_group_8_size:
                    temp_group_8.append(line)
                else:
                    plus = []
                    if isinstance(temp_group_8[0], str):
                        temp_group_8.insert(0, 00)
                        plus = [temp_group_8[-1]]
                        del temp_group_8[-1]
                    current_section.append(temp_group_8)
                    temp_group_8 = plus + [line]

        if current_section:
            if temp_group:
                current_section.insert(1, temp_group)
            if temp_group_8:
                if isinstance(temp_group_8[0], str):
                    temp_group_8.insert(0, 00)
                current_section.extend(temp_group_8)
            sections.append(current_section)

        del sections[0][1]
        del sections[1][1]
        del sections[2][1]
        del sections[3][1]

        if len(sections)==5 :
            del sections[4][1]
        
        poste = ["Gardien", "Défenseur", "Milieu", "Attaquant", "Poste non défini"]


        for i in range(4):
            for j in range(len(sections[i])): 
                if not isinstance(sections[i][j], list):
                    sections[i][j] = [sections[i][j]]
                sections[i][j] = [poste[i]] + sections[i][j]

        for i in range(4):
            for j in range(len(sections[i])):
                if not isinstance(sections[i][j], list):
                    sections[i][j] = [sections[i][j]]
                sections[i][j] = [club_name] + sections[i][j]
            del sections[i][len(sections[i])-1]
        
        del sections[0][0]
        del sections[1][0]
        del sections[2][0]
        del sections[3][0]

        if len(sections) == 5 :
            for j in range(len(sections[4])): 
                if not isinstance(sections[4][j], list):
                    sections[4][j] = [sections[4][j]]
                sections[4][j] = [poste[4]] + sections[4][j]

            for j in range(len(sections[4])):
                if not isinstance(sections[4][j], list):
                    sections[4][j] = [sections[4][j]]
                sections[4][j] = [club_name] + sections[4][j]
            del sections[4][len(sections[4])-1]

            del sections[4][0]
            del sections[4][-1]

        else : 
            del sections[3][-1]

        flattened_data = [player for section in sections for player in section]

        for player in flattened_data:
            player_data = {
                "club": player[0],
                "poste": player[1],
                "numero": player[2] ,
                "nom": player[3],
                "age": player[4],
                "matchs_joués": player[5],
                "buts": player[6],
                "passes_d": player[7] ,
                "stat_1": player[8] if len(player) > 8 else None,
                "stat_2": player[9] if len(player) > 9 else None
            }
            self.insert_player_data(player_data)