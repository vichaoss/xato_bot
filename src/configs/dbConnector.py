import sqlite3

from configs.settings import Settings


class DbConnector:
    connection = None

    @staticmethod
    def create_connection():
        try:
            DbConnector.connection = sqlite3.connect(Settings.database_file_path)
            pass
        except sqlite3.Error as e:
            print(e)
            pass
        return

    @staticmethod
    def __query_create_table_guilds():
        query = """
            CREATE TABLE IF NOT EXISTS guilds
            (
                guild_id   BLOB PRIMARY KEY,
                guild_name TEXT NOT NULL
            );
        """

        return query

    @staticmethod
    def __query_create_table_leagues():
        query = """
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

        return query

    @staticmethod
    def __query_create_table_members():
        query = """
            CREATE TABLE IF NOT EXISTS members
            (
                member_id       INTEGER PRIMARY KEY,
                member_user     TEXT NOT NULL
            );

        """
        return query

    @staticmethod
    def __query_create_table_members_of_league(league):
        query = "CREATE TABLE IF NOT EXISTS " + league.name + "_members(member_id BLOB PRIMARY KEY, member_nick TEXT, member_current_league INTEGER, FOREIGN KEY (member_current_league) REFERENCES leagues (league_id));"

        return query

    @staticmethod
    def __is_connected_to_database():
        return DbConnector.connection is not None

    @staticmethod
    def execute_query(query):
        if not DbConnector.__is_connected_to_database():
            return "Error, no connection to db"
            pass
        try:
            output = ""
            cursor = DbConnector.connection.cursor()
            try:
                cursor.execute(query)
                pass
            except Exception as e:
                return e
                pass
            info = cursor.fetchall()
            DbConnector.connection.commit()
            for value in info:
                output += str(value) + "\n"
                pass
            if output == "":
                return "No Output / Empty operation"
                pass
            return output
            pass
        except Exception as e:
            return e
            pass

    @staticmethod
    def startup():
        # TODO: no c ¿las tablas iniciales?
        pass

    pass
