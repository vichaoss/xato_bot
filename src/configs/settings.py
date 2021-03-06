# -*- coding: utf8 -*-
"""
Archivo que define las constantes y configurables del bot
"""
import os

from configs import botTokens


class Settings:
    VERSION = None
    servers = {"Wholesomness": 454838012908535808,
               "Servidor de pruebas": 760614553636962304}
    channels = {"Wholesomness": 801645015554195476,
                "Servidor de pruebas": 803265688076156988}
    ligas = ["Bronce", "Plata", "Oro", "Platino", "Diamante", "Challenger"]
    divisiones = [1, 2, 3, 4, 5]

    project_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    command_prefix = 'x!'

    # TODO: ponerle nombre al rol de xatAdmin
    admin_role = "XatAdmin"

    sources_folder_name = "src"
    resources_folder_name = "res"
    logs_folder_name = "logs"
    database_file_name = "database.db"

    sources_folder_path = os.path.join(project_folder_path, sources_folder_name)
    resources_folder_path = os.path.join(project_folder_path, resources_folder_name)
    logs_folder_path = os.path.join(project_folder_path, logs_folder_name)
    database_file_path = os.path.join(resources_folder_path, database_file_name)

    server_id = servers["Wholesomness"]
    channel_id = channels["Wholesomness"]

    token = botTokens.token_xato_bot

    guilds = None

    @staticmethod
    def startup(test=False):
        if test is True:
            Settings.server_id = Settings.servers["Servidor de pruebas"]
            Settings.channel_id = Settings.channels["Servidor de pruebas"]
            pass
        try:
            os.makedirs(Settings.resources_folder_path)
        except FileExistsError:
            pass
        open(Settings.database_file_path, "a").close()
        return

    pass
