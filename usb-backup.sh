#!/bin/bash

# Incremental backup of a usb flash drive on the current date
# The script is executed by a user with root rights (sudoers)
# Required utilities: mount, tar, gzip, tee

function write_log() {
  echo -e "$1" | tee -a $BACKUP_PATH/$LOG_FILE
}

# Directory of source files for archiving, '/' at the end, it is mandatory
SOURCE_PATH=/path/to/usb-drive/
# The mounting point of the disk on which the archive will be located
MOUNT_POINT=/path/to/mount/point
# The path to the backup directory at the mount point
BACKUP_PATH=$MOUNT_POINT/path/to/dir/backup
# Creating a file name for the current date
BACKUP_FILE=usb.$(date +%Y-%m-%d).tar.gz
LOG_FILE=archive.log
UUID=01DB2557286B1350 # UUID backup disk (for mount command)

# Mount if there is no mounting path
if [[ ! -e $BACKUP_PATH ]]; then
  echo "Mount $BACKUP_PATH"
  sudo mount -U $UUID $MOUNT_POINT -o uid=1000,gid=1000
fi

# Log entry datetime identifier
write_log "\n*** $(date +%Y-%m-%d' '%H:%S) ***\n"

# If the archive for the current date exists,
# then write to the log and exit with the code 2
[[ -e $BACKUP_PATH/$BACKUP_FILE ]] &&
  write_log "File $BACKUP_FILE already exists in directory $BACKUP_PATH, skip" &&
  exit 2

write_log "Creating archive $BACKUP_FILE"

# Run tar and check result code
if tar -czvf $BACKUP_PATH/"$BACKUP_FILE" -g $BACKUP_PATH/usb.snar \
  -X $BACKUP_PATH/.backupignore $SOURCE_PATH 2>>$BACKUP_PATH/$LOG_FILE; then
  write_log "Create arhive success"
else
  write_log "Error during create archive"
fi
