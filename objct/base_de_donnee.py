# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from objct.logger import logger


class Database:
    """
    S'occupe de maintenir une connexion à une base de données SQLite3 et d'exécuter des requêtes
    """

    def __init__(self, database_location):
        """
        Crée une nouvelle instance de `Database` et établit une connexion à la base de données.
        :param database_location: Chemin du fichier contenant la base de données
        """
        logger.log("DATABASE", "Connection à la base de données {}".format(database_location))
        self.conn = sqlite3.connect(database_location)

    def _run_query(self, query):
        """
        Exécute une requête sur la base de données
        :param query: Requête SQL à exécuter
        :return: Un array avec le résultat de la requête.
                 Retourne un tableau vide pour les CREATE et INSERT
        """
        logger.log("DATABASE", "Requête: {}".format(query))
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        data = cursor.fetchall()
        return data

    def insert_speed(self, value, time):
        """
        Insert une nouvelle vitesse dans la base de données
        :param value: Valeur de la vitesse à insérer
        :param time: Temps à lequel la vitesse a été reçu
        """
        query = "INSERT INTO mondon_speed VALUES ({time}, {speed})".format(time=time, speed=value)
        self._run_query(query)
