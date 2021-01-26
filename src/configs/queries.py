# TODO: docstring

class Queries:

    @staticmethod
    def count_rows_on_leagues():
        return """SELECT COUNT(*) FROM leagues"""

    @staticmethod
    def populate_leagues_table():
        ligas = {1: "Bronce 5", 2: "Bronce 4", 3: "Bronce 3", 4: "Bronce 2", 5: "Bronce 1",
                 6: "Plata 5", 7: "Plata 4", 8: "Plata 3", 9: "Plata 2", 10: "Plata 1",
                 11: "Oro 5", 12: "Oro 4", 13: "Oro 3", 14: "Oro 2", 15: "Oro 1",
                 16: "Platino 5", 17: "Platino 4", 18: "Platino 3", 19: "Platino 2", 20: "Platino 1",
                 21: "Diamante 5", 22: "Diamante 4", 23: "Diamante 3", 24: "Diamante 2", 25: "Diamante 1",
                 26: "Challenger"
                 }

        query = 'INSERT INTO leagues(league_id, league_name, league_next, league_previous) VALUES'
        for liga in ligas:
            if liga == 1:
                query = query + "(" + str(liga) + ",'" + ligas[liga] + "'," + str((liga + 1)) + ",NULL),"
                continue
            if liga == 26:
                query = query + "(" + str(liga) + ",'" + ligas[liga] + "',NULL," + str((liga - 1)) + ");"
                continue
            query = query + "(" + str(liga) + ",'" + ligas[liga] + "'," + str((liga + 1)) + "," + str((liga - 1)) + "),"

        return query

    @staticmethod
    def create_table_guilds():
        return """
            CREATE TABLE IF NOT EXISTS guilds
            (
                guild_id   BLOB PRIMARY KEY,
                guild_name TEXT NOT NULL
            );
        """

    @staticmethod
    def create_table_leagues():
        return """
            CREATE TABLE IF NOT EXISTS leagues
            (
                league_id       INTEGER PRIMARY KEY,
                league_name     TEXT NOT NULL,
                league_next     INTEGER,
                league_previous INTEGER,
                FOREIGN KEY (league_next) REFERENCES leagues (league_id),
                FOREIGN KEY (league_previous) REFERENCES leagues (league_id)
            );
        """

    @staticmethod
    def create_table_members():
        return """
            CREATE TABLE IF NOT EXISTS members
            (
                member_id       INTEGER PRIMARY KEY,
                member_user     TEXT NOT NULL,
                current_league  INTEGER,
                FOREIGN KEY (current_league) REFERENCES leagues(league_id)
            );

        """


pass
