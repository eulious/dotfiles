BACKUP=/Volumes/2TB/Backup
BACKUP2=/Volumes/3TB/Backup

backup_daily(){
    echo LastBackup: `cat $BACKUP/.backuplog`
    date | sed -e "s/JST//" > $BACKUP/.backuplog
    echo "From ~/Desktop To $BACKUP"
    rsync -a --delete ~/Desktop $BACKUP
    echo "From ~/www To $BACKUP"
    rsync -a --delete --exclude "node_modules/*" ~/www $BACKUP
}

backup(){
    echo LastBackup: `cat $BACKUP2/.backuplog`
    date | sed -e "s/JST//" > $BACKUP2/.backuplog
    echo "BACKUP2"
    rsync -a --delete $BACKUP $BACKUP2
}

backup2(){
    echo LastBackup: `cat $BACKUP/.backuplog2`
    date | sed -e "s/JST//" > $BACKUP/.backuplog2
    echo "Now copying ~/Library/CELSYS"
    rsync -a --delete ~/Library/CELSYS $BACKUP
    echo "Now copying /Library/Audio/Presets/Xfer\ Records/Serum\ Presets"
    rsync -a --delete /Library/Audio/Presets/Xfer\ Records/Serum\ Presets $BACKUP
}