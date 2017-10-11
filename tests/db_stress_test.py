from random import randint
from threading import Thread
from time import sleep, time

from objct.base_de_donnee import Database
from objct.logger import logger


THREAD_NUM = 20
logger.log_app_start()


def make_log_fn(thread_name):
    def log_fn(log_text):
        logger.log('DB_STRESS_TEST', '{} | {}'.format(thread_name.ljust(10), log_text))
    return log_fn


def thread_func(log_fn):
    db = Database('../../mondon.db')
    log_fn('created')
    while True:
        # sleep_time = randint(1, 5) / 1000.0
        # log_fn('sleeping ({} ms)'.format(str(sleep_time).ljust(5)))
        # sleep(sleep_time)
        new_speed = randint(1, 200)
        new_time = int(round(time() * 1000))
        log_fn('inserting ({}, {})'.format(new_speed, new_time))
        try:
            db.insert_speed(new_speed, new_time)
            log_fn('inserted ({}, {})'.format(new_speed, new_time))
        except Exception as e:
            log_fn('failed for ({}, {}), error:\n{}\n{}\n\n\n'
                   .format(new_speed, new_time, e.__class__.__name__, e))


# Démarre les threads qui écrivent dans la base de données
threads = [
    Thread(target=thread_func,
           args=([make_log_fn('Thread_{}'.format(i + 1))]))
    for i in range(THREAD_NUM)
]
for thread in threads:
    thread.start()
