# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QMainWindow

from objct.base_de_donnee import *
from datetime import datetime
import locale
import time


class MainWindow(QMainWindow):
    """
    Fenêtre Qt.
    Se charge de plusieurs choses :
    - Récupérer les nouvelles vitesses et les insérer dans la base de données
    - Afficher l'heure à laquelle on a reçu la dernière vitesse
    - Afficher la dernière vitesse insérée dans la base de données ou une erreur si quelque chose
      s'est mal passé.
    """

    SLEEP_ON_ERROR_MS = 1000  # Temps d'attent en millisecondes en cas d'erreur avant de réessayer.

    def __init__(self, database):
        """
        Crée une nouvelle instance de `QMainWindow`
        :param database: instance de la base de données
        """
        super(MainWindow, self).__init__()
        self.database = database
        # Label qui affiche la dernière vitesse (ou un message d'erreur)
        self.label = QLabel(self)
        self.label.setGeometry(15, 20, 220, 30)
        # Label qui affiche l'heure
        self.label2 = QLabel(self)
        self.label2.setGeometry(15, 0, 220, 30)

    def watch_signal(self, new_speed_signal):
        """
        Écoute un signal et exécute la fonction `handle_new_speed` à chaque fois que le signal
        émet de nouvelles valeurs
        :param new_speed_signal: Signal à écouter
        """
        new_speed_signal.connect(self.handle_new_speed)

    @staticmethod
    def timestamp_to_hour(millitimestamp):
        """
        Utilitaire pour convertir un millitimestamp en heure.
        :param millitimestamp: le millitimestamp à convertir
        :return: Un string au format "<heures>:<minutes>:<secondes>" ou "??:??:??" en cas d'erreur
        """
        ts = millitimestamp / 1000
        try:
            locale.setlocale(locale.LC_TIME, '')
            return datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        except:
            return '??:??:??'

    @staticmethod
    def timestamp_to_date(millitimestamp):
        """
        Utilitaire pour convertir un millitimestamp en date + heure.
        :param millitimestamp: le millitimestamp à convertir
        :return: Un string au format
                 "<années>:<mois>:<jours> <heures>:<minutes>:<secondes>.<millisecondes>"
                 ou "????-??-?? ??:??:??" en cas d'erreur.
        """
        ts = millitimestamp / 1000
        try:
            locale.setlocale(locale.LC_TIME, '')
            return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
        except:
            return '????-??-?? ??:??:??'

    def handle_new_speed(self, speed_value, ts, retry_on_failure=True):
        """
        Gère la réception de nouvelle vitesse.
        La nouvelle vitesse est d'abord insérée dans la base de données. En cas d'erreur, la
        fonction réessayera une nouvelle fois avant d'abandonner.
        Les labels sont en suite mis à jour avec les dernières valeurs
        :param speed_value: Nouvelle vitesse
        :param ts: Millitimestamp de quand on a reçu la vitesse
        :param retry_on_failure: Contrôle si l'on doit réessayer l'insertion dans la base de
                                 donnée en cas d'erreur.
        """
        logger.log("MAIN_WINDOW", "Insert vitesse {} au temps {}"
                   .format(speed_value, MainWindow.timestamp_to_date(ts)))
        try:
            self.database.insert_speed(speed_value, ts)
            self.label.setText("Mise à jour : vitesse = {} m/min".format(speed_value))
        except Exception as e:
            self.label.setText("Erreur base de données")
            logger.log("MAIN_WINDOW", "Erreur lors de l'insertion dans la base de données: {}"
                       .format(e))
            if retry_on_failure:
                logger.log("MAIN_WINDOW", "Pause pendant {} ms et réessaye"
                           .format(MainWindow.SLEEP_ON_ERROR_MS))
                time.sleep(MainWindow.SLEEP_ON_ERROR_MS * 1000)
                self.handle_new_speed(speed_value, ts, retry_on_failure=False)
            else:
                logger.log("MAIN_WINDOW", "Abandon")

        hours = MainWindow.timestamp_to_hour(ts)
        self.label2.setText(hours)
