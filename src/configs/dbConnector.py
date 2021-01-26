import sqlite3

from configs.queries import Queries
from configs.settings import Settings


class DbConnector:

    @staticmethod
    def create_connection():
        try:
            return sqlite3.connect(Settings.database_file_path)
        except sqlite3.Error as e:
            print(e)
            pass
        return None

    @staticmethod
    def execute_query(query):
        connection = DbConnector.create_connection()
        if connection is None:
            return "Error, no connection to db"
            pass
        try:
            output = ""
            cursor = connection.cursor()
            cursor.execute(query)
            info = cursor.fetchall()
            connection.commit()
            for value in info:
                output += str(value) + "\n"
                pass
            if output == "":
                cursor.close()
                connection.close()
                return "No Output / Empty operation"
                pass
            cursor.close()
            connection.close()
            return output
            pass
        except Exception as e:
            connection.close()
            return e
            pass
        pass

    @staticmethod
    def is_league_table_populated():
        connection = DbConnector.create_connection()
        if connection is None:
            return False
            pass
        try:
            cursor = connection.cursor()
            cursor.execute(Queries.count_rows_on_leagues())
            result = cursor.fetchone()

            if result[0] == 0:
                cursor.close()
                connection.close()
                return False
                pass
        except Exception as e:
            connection.close()
            return e
        return True
        pass

    @staticmethod
    def startup():
        DbConnector.execute_query(Queries.create_table_leagues())
        DbConnector.execute_query(Queries.create_table_members())
        if not DbConnector.is_league_table_populated():
            DbConnector.execute_query(Queries.populate_leagues_table())
            pass
        return

    @staticmethod
    def register(id_player_to_add, nick_player_to_add, league_to_add):
        connection = DbConnector.create_connection()
        if connection is None:
            return False
            pass
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT league_id FROM leagues WHERE league_name LIKE ?", [league_to_add])
            liga = cursor.fetchone()
            cursor.execute("INSERT INTO members(member_id, member_user, current_league) VALUES (?,?,?);",
                           (id_player_to_add, nick_player_to_add, liga[0]))
            connection.commit()
            cursor.close()
            connection.close()
            return
        except Exception as e:
            print(e)
            connection.close()
            return e
        pass

    @staticmethod
    def fetch_players():
        connection = DbConnector.create_connection()
        if connection is None:
            return []
            pass
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT member_id FROM members;")
            resultado = cursor.fetchall()
            cursor.close()
            connection.close()
            return resultado
        except sqlite3.Error:
            connection.close()
            return []
        pass

    @staticmethod
    def fetch_leaderboard():
        connection = DbConnector.create_connection()
        if connection is None:
            return []
            pass
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT member_user,current_league FROM members ORDER BY current_league DESC ;")
            resultado = cursor.fetchall()
            arr = []
            for res in resultado:
                cursor.execute("SELECT league_name FROM leagues WHERE league_id LIKE ?", [res[1]])
                aux = cursor.fetchone()
                arr.append([res[0], aux[0]])
            cursor.close()
            connection.close()
            return arr
        except sqlite3.Error:
            connection.close()
            return []
        pass

    @staticmethod
    def change_alias(member_id, new_member_name):
        connection = DbConnector.create_connection()
        if connection is None:
            return []
            pass
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE members SET member_user = ? WHERE member_id = ?;",
                           (new_member_name, member_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error:
            connection.close()
            return False
        pass

    @staticmethod
    def downgrade_user(member_id):
        connection = DbConnector.create_connection()
        if connection is None:
            return None
            pass
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT current_league FROM members WHERE member_id=?", [member_id])
            res = cursor.fetchone()
            cursor.execute("SELECT league_previous FROM leagues WHERE league_id=?", [int(res[0])])
            res = cursor.fetchone()
            cursor.execute("UPDATE members SET current_league = ? WHERE member_id = ?;",
                           (int(res[0]), member_id))
            cursor.execute("SELECT league_name FROM leagues WHERE league_id=?", [int(res[0])])
            res = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            return res[0]
        except sqlite3.Error:
            connection.close()
            return None
        pass

    @staticmethod
    def promote_user(member_id):
        connection = DbConnector.create_connection()
        if connection is None:
            return None
            pass
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT current_league FROM members WHERE member_id=?", [member_id])
            res = cursor.fetchone()
            cursor.execute("SELECT league_next FROM leagues WHERE league_id=?", [int(res[0])])
            res = cursor.fetchone()
            cursor.execute("UPDATE members SET current_league = ? WHERE member_id = ?;",
                           (int(res[0]), member_id))
            cursor.execute("SELECT league_name FROM leagues WHERE league_id=?", [int(res[0])])
            res = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            return res[0]
        except sqlite3.Error:
            connection.close()
            return None
        pass


pass
