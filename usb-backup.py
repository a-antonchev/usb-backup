#!/home/antonchev/opt/miniconda3/envs/common/bin/python3

# прикрутить архивы
# прикрутить logging

import os
import os.path
from datetime import datetime
from getpass import getpass
import subprocess

MOUNT_POINT = '/mnt/store'
PATH_SOURCE = '/media/antonchev/USB-накопитель'
PATH_BACKUP = MOUNT_POINT + '/Backup'
FILE_BACKUP = f'usb.{datetime.strftime(datetime.today(), "%Y-%m-%d")}.tar.gz'
cmd_mount = ['sudo', '-S', 'mount', '-U', '01DB2557286B1350', '/mnt/store', '-o', 'uid=1000,gid=1000']
cmd_arch = ['tar',
   '-czvf', PATH_BACKUP + '/' + FILE_BACKUP,
    '-g', PATH_BACKUP + '/usb.snar',
    '-X', PATH_BACKUP + '/.backupignore', PATH_SOURCE + '/*']

if not os.path.ismount(MOUNT_POINT):
    password = getpass("Enter your password: ")
    try:
        proc = subprocess.run(
            cmd_mount,
            input=password.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)
    except subprocess.CalledProcessError as err:
        print(err.__str__())
    else:
        if os.path.exists(f'{PATH_BACKUP}/{FILE_BACKUP}'):
            print(f'Архив {FILE_BACKUP} уже существует')
        else:
            print(f'Создаем архив {PATH_BACKUP}/{FILE_BACKUP}')
            try:
                proc = subprocess.run(
                    cmd_arch,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True)
            except subprocess.CalledProcessError as err:
                print(err.__str__())
