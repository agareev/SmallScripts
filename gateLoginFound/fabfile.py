from fabric.api import run, env, roles

import psutil
import re

env.roledefs['test'] = ['root@devsupport']
proc = "[i]ssgate"
# proc = "nginx"


env.hosts = ['root@devsupport']


def host_type():
    """
    Определение host
    """
    run('hostname')

def check_process(name="nginx"):
    """
    Проверка на наличие процесса
    """
    issgate_pids = run('ps -ef|grep {}'.format(name))
    if issgate_pids != "":
        print(issgate_pids)
    else:
        print("noo")



def _find_config():
    """
    Поиск файла логина
    """
    pass


def _grep_login():
    """
    Поиск логина в конфиг файле
    """
    pass


def get_login_list():
    """
    Получение списка используемых логинов
    """
    print("DONE")
