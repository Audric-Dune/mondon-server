# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QThread
from random import randint
import socket
import time

from objct.automate_command import CONNECT, GET_SPEED
from objct.logger import logger


class SpeedThread(QThread):
    """
    Thread qui se charge de se connecter à l'automate et de communiquer avec lui.
    """
    SLEEP_TIME_MS = 240
    SLEEP_ON_ERROR_MS = 1000
    NEW_SPEED_SIGNAL = pyqtSignal('unsigned long long', 'unsigned long long')

    def __init__(self, automate_ip, automate_port):
        """
        Crée une nouvelle instance de SpeedThread
        """
        QThread.__init__(self)
        self.socket = None
        self.automate_ip = automate_ip
        self.automate_port = automate_port

    def _init_socket(self):
        """
        Crée une nouvelle socket (et ferme la socket courante si il y en a une) et connecte la
        à l'automate.
        """
        logger.log("SPEED_THREAD", "Initialization de la socket")
        if self.socket:
            logger.log("SPEED_THREAD", "Socket déjà initialisée, fermeture de la socket")
            self.socket.close()
        logger.log("SPEED_THREAD", "Création d'une socket")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.log("SPEED_THREAD", "Connexion à {}:{}"
                   .format(self.automate_ip, self.automate_port))
        self.socket.connect((self.automate_ip, self.automate_port))

    def _send_to_automate(self, command):
        """
        Envoi une commande à l'automate
        :param command: Commande a envoyer à l'automate
        """
        logger.log("SPEED_THREAD", 'Envoi de la commande {} ({})'
                   .format(command.description, command.hex))
        self.socket.sendall(command.binary)

    def _receive_from_automate(self):
        """
        Attends un message de l'automate
        :return: Retourne le message reçu de l'automate. Retourne un string vide si rien n'a
                 été reçu.
        """
        response = self.socket.recv(1024)
        logger.log("SPEED_THREAD", "Reçu de l'automate: {}".format(response))
        return response

    def _connect(self):
        """
        Initialise la connexion à l'automate
        """
        self._init_socket()  # Création de la socket
        self._send_to_automate(CONNECT)  # Envoi du message initial de connexion
        response = self._receive_from_automate()
        # L'automate est supposé retourner un message non vide si la connexion est correctement
        # établie.
        if not response:
            raise Exception("Réponse invalide après tentative de connexion à l'automate: {}"
                            .format(response))

    def _get_speed(self):
        """
        Récupère la vitesse courante de l'automate.
        :return: la vitesse de l'automate.
        """
        self._send_to_automate(GET_SPEED)
        response = self._receive_from_automate()
        if not response:
            raise Exception("Réponse invalide après tentative de récupération de "
                            "la vitesse de l'automate: {}"
                            .format(response))
        mondon_speed = int.from_bytes(response[-4:], byteorder="big")
        logger.log("SPEED_THREAD", "Nouvelle vitesse reçue: {}".format(mondon_speed))
        return mondon_speed

    def run(self):
        """
        Méthode principale qui sera exécuter sur un nouveau thread.
        Se charge d'établir une connexion à l'automate et de récupérer la vitesse courante
        toutes les `SLEEP_TIME_MS` millisecondes.
        En cas d'erreur, un pause de `SLEEP_ON_ERROR_MS` millisecondes est prise avant de
        recommencer (depuis le début, création de la connexion incluse).
        """
        try:
            self._connect()
            while True:
                # Récupération de la vitesse
                ts_before_get_speed = time.time()
                mondon_speed = self._get_speed()
                ts_after_get_speed = time.time()

                # Calcule combien de temps on a mis à récupérer la vitesse
                delay = ts_after_get_speed - ts_before_get_speed

                # Émets une nouvelle paire timestamp/vitesse
                ts = int(round(ts_after_get_speed * 1000))
                self.NEW_SPEED_SIGNAL.emit(mondon_speed, ts)

                # Pause pendant SpeedThread.SLEEP_TIME_MS (moins le temps qu'il a fallu pour
                # récupérer la vitesse.
                self.msleep(max(0, SpeedThread.SLEEP_TIME_MS - delay))
        except Exception as e:
            logger.log("SPEED_THREAD", "Erreur: {}".format(e))
            self.msleep(SpeedThread.SLEEP_ON_ERROR_MS)
            self.run()


class SpeedThreadSimulator(SpeedThread):
    """
    Thread qui hérite de SpeedThread et qui redéfinit les fonctions `_connect` et `_get_speed`
    pour simuler l'automate en locale.
    """
    def _connect(self):
        """
        Simule la connexion à l'automate. Ne fait rien à part un log.
        """
        logger.log("SPEED_THREAD", "Simulation d'une connexion à l'automate")

    def _get_speed(self):
        """
        Simule la récupération d'une nouvelle vitesse en générant une valeur aléatoire.
        Simule une erreur de manière aléatoire 1% du temps.
        :return:
        """
        if randint(0, 100) == 1:
            raise Exception("Simulation d'une erreur!!")
        random_speed = randint(0, 185)
        logger.log("SPEED_THREAD", "Génération d'une vitesse aléatoire ({})"
                   .format(random_speed))
        return random_speed
