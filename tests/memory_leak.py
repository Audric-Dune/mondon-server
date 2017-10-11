from itertools import groupby
import operator
import resource
from pympler import tracker, muppy, summary
from random import randint
from threading import Thread
from time import time, sleep

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from objct.base_de_donnee import Database
from objct.logger import logger
from objct.main_window import MainWindow
from objct.speed_thread import SpeedThreadSimulator


def memory_usage_thread_func():
    tr = tracker.SummaryTracker()
    sleep(20)
    first_summary = tr.create_summary()
    while True:
        latest_summary = tr.create_summary()
        tr.print_diff(summary1=first_summary, summary2=latest_summary)
        self_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1000 * 1000)
        print('Memory usage: {} Mb'.format(self_use))
        sleep(10)

Thread(target=memory_usage_thread_func).start()


logger.log_app_start()

logger.log("INITIALISATION", "Création de la QApplication avec les paramètres: {}".format(sys.argv))
app = QApplication(sys.argv)

logger.log("INITIALISATION", "Définition de l'icone de l'application")
app.setWindowIcon(QIcon('icon/logo_get_speed.ico'))

logger.log("INITIALISATION", "Initialisation de Database")
db = Database('../../mondon.db')

logger.log("INITIALISATION", "Création de MainWindow")
window = MainWindow(database=db)

logger.log("INITIALISATION", "Configuration de MainWindow")
window.setFixedSize(250, 50)
window.setWindowTitle("Get speed")

logger.log("INITIALISATION", "Affichage de MainWindow")
window.show()

logger.log("INITIALISATION", "Création de SpeedThread (Simulator)")
speed_thread = SpeedThreadSimulator(automate_ip=None, automate_port=None)

logger.log("INITIALISATION", "MainWindow écoute SpeedThread")
window.watch_signal(speed_thread.NEW_SPEED_SIGNAL)

logger.log("INITIALISATION", "Démarrage de SpeedThread")
speed_thread.start()

sys.exit(app.exec_())

# def insert_in_db():
#     new_speed = randint(1, 200)
#     new_time = int(round(time() * 1000))
#     # print('inserting ({}, {})'.format(new_speed, new_time))
#     try:
#         db.insert_speed(new_speed, new_time)
#         # print('inserted ({}, {})'.format(new_speed, new_time))
#     except Exception as e:
#         print('failed for ({}, {}), error:\n{}\n{}\n\n\n'
#               .format(new_speed, new_time, e.__class__.__name__, e))



# dicts = [repr(ao) for ao in all_objects if isinstance(ao, dict)]
# grouped = [(len(list(v)), k) for k, v in groupby(sorted(dicts))]
# sorted_group = reversed(sorted(grouped, key=operator.itemgetter(0)))
# for data in sorted_group:
#     print(str(data[0]).ljust(5), data[1][:100])


# strs = [ao for ao in all_objects if isinstance(ao, str)]
# grouped = [(len(list(v)), k) for k, v in groupby(sorted(strs))]
# sorted_group = reversed(sorted(grouped, key=operator.itemgetter(0)))
#
# for data in sorted_group:
#     print(str(data[0]).ljust(5), data[1])
