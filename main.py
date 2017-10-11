# !/usr/bin/env python
# -*- coding: utf-8 -*-

from objct.logger import logger
logger.log_app_start()

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from objct.main_window import MainWindow
from objct.speed_thread import SpeedThread, SpeedThreadSimulator
from objct.base_de_donnee import Database


SIMULATOR_ON = True  # Définit si l'on simule la connexion à l'automate


logger.log("INITIALISATION", "Création de la QApplication avec les paramètres: {}".format(sys.argv))
app = QApplication(sys.argv)

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon('icon/logo_get_speed.ico'))

logger.log("INITIALISATION", "Initialisation de Database")
db = Database('../mondon.db')

logger.log("INITIALISATION", "Création de MainWindow")
window = MainWindow(database=db)

logger.log("INITIALISATION", "Configuration de MainWindow")
window.setFixedSize(250, 50)
window.setWindowTitle("Get speed")

logger.log("INITIALISATION", "Affichage de MainWindow")
window.show()

logger.log("INITIALISATION", "Création de SpeedThread{}"
           .format(" (Simulator)" if SIMULATOR_ON else ""))
if SIMULATOR_ON:
    speed_thread = SpeedThreadSimulator(automate_ip=None, automate_port=None)
else:
    speed_thread = SpeedThread(automate_ip="192.168.0.50", automate_port=9600)

logger.log("INITIALISATION", "MainWindow écoute SpeedThread")
window.watch_signal(speed_thread.NEW_SPEED_SIGNAL)

logger.log("INITIALISATION", "Démarrage de SpeedThread")
speed_thread.start()

sys.exit(app.exec_())