#!/usr/bin/env python3

# Incremental backup of a usb flash drive on the current date
# The script is executed by a user with root rights (sudoers)

import os.path
from datetime import datetime
from getpass import getpass
import subprocess
import logging
import shutil

# Directory of source files for archiving, '/' at the end, it is mandatory
source_path = '/path/to/usb-drive/'
# The mounting point of the disk on which the archive will be located
mount_point = '/path/to/mount/point'
# The path to the backup directory at the mount point
backup_dir = f'{mount_point}/path/to/backup/dir'
today = datetime.strftime(datetime.today(), "%Y-%m-%d")
# Creating a file name for the current date
backup_file = f'usb.{today}.tar.gz'
# Full path for backup file
backup_path = f'{backup_dir}/{backup_file}'

cmd_mount = ['sudo', '-S', 'mount', '-U', '01DB2557286B1350',
             '/mnt/store', '-o', 'uid=1000,gid=1000']
cmd_arch = ['tar', '-czvf', backup_path, '-g', f'{backup_dir}/usb.snar',
            '-X', f'{backup_dir}/.backupignore', source_path]

# Mount if there is no mounting path
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

# Init logging
log_file = f'{backup_dir}/archive.log'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('backup')
file_handler = logging.FileHandler(log_file)
logger.addHandler(file_handler)

# Log entry datetime identifier
logger.info(f'\n*** {today} ***\n')

# If the archive for the current date exists,
# then write to the log and exit with the code 2
if os.path.exists(f'{backup_path}'):
    logger.info(f'File {backup_file} already exists in directory, skip.')
    raise SystemExit(2)
else:
    logger.info(f'Creating archive {backup_file}')
    # Due to the fact that the 'tar' command, if executed unsuccessfully, creates
    # an archive anyway and makes changes to the incremental updates file 'usb.snar',
    # we create a copy of 'usb.snap.save'
    shutil.copy(f'{backup_dir}/usb.snar', f'{backup_dir}/usb.snar.save')
    try:
        proc = subprocess.run(
            cmd_arch,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)
    except subprocess.CalledProcessError as err:
        logger.info('Error during create archive')
        logger.info(err.__str__())
        # Error - rollback 'usb.snap.save'
        shutil.move(f'{backup_dir}/usb.snar.save', f'{backup_dir}/usb.snar')
        # Error - remove bad archive
        os.remove(backup_path)
        raise SystemExit(3)
    else:
        logger.info('Create arhive success')
        # Success - remove 'usb.snap.save'
        os.remove(f'{backup_dir}/usb.snar.save')
