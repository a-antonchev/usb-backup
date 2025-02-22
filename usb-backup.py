#!/usr/bin/env python3

import os.path
from datetime import datetime
from getpass import getpass
import subprocess
import logging

source_path = '/path/to/usb-drive/'
mount_point = '/path/to/mount/point'
backup_dir = f'{mount_point}/path/to/backup/dir'
today = datetime.strftime(datetime.today(), "%Y-%m-%d")
backup_file = f'usb.{today}.tar.gz'
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
    print(f'Mount {backup_dir}')
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
        raise SystemExit(1)

log_file = f'{backup_dir}/archive.log'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('backup')
file_handler = logging.FileHandler(log_file)
logger.addHandler(file_handler)

logger.info(f'\n*** {today} ***\n')

if os.path.exists(f'{backup_path}'):
    logger.info(f'File {backup_file} already exists in directory, skip.')
    raise SystemExit(2)
else:
    logger.info(f'Creating archive {backup_file}')
    try:
        proc = subprocess.run(
            cmd_arch,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)
    except subprocess.CalledProcessError as err:
        logger.info('Error during create archive')
        logger.info(err.__str__())
        raise SystemExit(3)
    else:
        logger.info('Create arhive success')
