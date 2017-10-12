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
    - Afficher l'heure à laquelle on a reçu la dernière vitesse
    - Afficher la dernière vitesse insérée dans la base de données ou une erreur si quelque chose
      s'est mal passé.
    """

    def __init__(self):
        """
        Crée une nouvelle instance de `QMainWindow`
        """
        super(MainWindow, self).__init__()
        # Label qui affiche la dernière vitesse (ou un message d'erreur)
        self.label = QLabel(self)
        self.label.setGeometry(15, 20, 370, 30)
        # Label qui affiche l'heure
        self.label2 = QLabel(self)
        self.label2.setGeometry(15, 0, 370, 30)

    def watch_signals(self, new_speed_signal, error_signal):
        """
        Écoute les signaux et exécute les fonction `handle_new_speed` et `handle_error` à chaque
        fois que les signaux émettent de nouvelles valeurs
        :param new_speed_signal: Signal qui se déclenche quand l'on a reçu une nouvelle qui a été
                                 insérée avec succès dans la base de données
        :param error_signal: Signal qui se déclenche lorsqu'une erreur s'est produite durant la
                             récupération ou la sauvegarde d'une vitesse
        """
        new_speed_signal.connect(self.handle_new_speed)
        error_signal.connect(self.handle_error)

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

    def handle_new_speed(self, speed_value, ts):
        """
        Met à jour les labels lorsqu'une nouvelle vitesse à été insérée
        :param speed_value: La nouvelle vitesse
        :param ts: Le timestamp en milliseconde de quand on a reçu la vitesse
        """
        hours = MainWindow.timestamp_to_hour(ts)
        self.label.setText("Mise à jour : vitesse = {} m/min".format(speed_value))
        self.label2.setText(hours)

    def handle_error(self, error):
        """
        Met à jour les labels lorsqu'une erreur se produit durant la récupération ou la sauvegarde
        d'une nouvelle vitesse.
        :param error: L'erreur qui s'est produite
        """
        self.label.setText(error)
