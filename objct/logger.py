import os
from datetime import datetime


class Logger:
    """
    S'occupe de créer et maintenir des fichiers de logs
    """
    def __init__(self, log_directory_location):
        """
        Crée une nouvelle instance de `Logger`
        :param log_directory_location: Chemin du dossier ou les fichiers de log seront stockés.
                                       Si le dossier n'existe pas, il sera automatiquement créé
        """
        self.log_directory_location = log_directory_location
        self._create_log_directory_if_not_exists()

    def _create_log_directory_if_not_exists(self):
        """
        Crée le dossier pour les fichiers de log si il n'existe pas.
        """
        if not os.path.exists(self.log_directory_location):
            os.makedirs(self.log_directory_location)

    def _get_log_file_location(self):
        """
        Génère le chemin où le fichier de log courant est stocké.
        Le nom du fichier est dérivé de la date courante.
        :return: Le chemin vers le fichier de log
        """
        now = datetime.now()
        file_name = now.strftime('%Y-%m-%d.txt')
        return self.log_directory_location + '/' + file_name

    def _write_to_log_file(self, text):
        """
        Log dans le fichier de log courant. Si le fichier n'existe pas,
        il sera crée automatiquement.
        :param text: Texte à insérer dans le fichier de log
        """
        file_location = self._get_log_file_location()
        file = open(file_location, 'a')
        file.writelines(text + "\n")
        file.flush()

    def _date_and_time(self):
        """
        :return: Un string représentant le temps actuel
        """
        now = datetime.now()
        date_and_time = now.isoformat()
        return date_and_time

    def log(self, log_category, log_text):
        """
        Méthode principale pour les log.
        Ajoute à la fin du fichier de log courant une nouvelle ligne avec le format suivant:
        "[<temps>] | <category> | <message>"
        Note: Si quelque chose se passe mal durant le log, on ignore l'erreur et ne log rien
        :param log_category: Catégorie du message de log
        :param log_text: Message à log
        """
        try:
            category = log_category.ljust(14)
            date_and_time = self._date_and_time()
            to_log = '[{}] | {} | {}'.format(date_and_time, category, log_text)
            self._write_to_log_file(to_log)
        except:
            pass

    def log_app_start(self):
        """
        Méthode spécial pour log le démarrage de l'application avec un format spécial
        """
        date_and_time = self._date_and_time()
        to_log = '\n\n\n------- APP START [{}] -------\n\n\n'.format(date_and_time)
        self._write_to_log_file(to_log)


logger = Logger('./logs')
