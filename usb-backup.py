#!/usr/bin/env python3

import os.path
from datetime import datetime
from getpass import getpass
import subprocess

source_path = '/path/to/usb-drive/'
mount_point = '/path/to/mount/point'
backup_dir = f'{mount_point}/path/to/backup/dir'
backup_file = f'usb.{datetime.strftime(datetime.today(), "%Y-%m-%d")}.tar.gz'
backup_path = f'{backup_dir}/{backup_file}'

cmd_mount = ['sudo', '-S', 'mount', '-U', '01DB2557286B1350', '/mnt/store', '-o', 'uid=1000,gid=1000']
cmd_arch = [
    'tar',
   '-czvf', backup_path,
    '-g', f'{backup_dir}/usb.snar',
    '-X', f'{backup_dir}/.backupignore',
    source_path
]

if not os.path.ismount(mount_point):
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
    if os.path.exists(f'{backup_path}'):
        print(f'Архив {backup_file} уже существует')
    else:
        print(f'Создаем архив {backup_path}/{backup_file}')
        try:
            proc = subprocess.run(
                cmd_arch,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True)
        except subprocess.CalledProcessError as err:
            print(err.__str__())
