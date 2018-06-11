BACKUP=/Volumes/書庫２/予備
backup(){
    echo LastBackup: `cat $BACKUP/.backuplog`
    date | sed -e "s/JST//" > $BACKUP/.backuplog
    echo "From ~/Dropbox To $BACKUP"
    rsync -a --delete ~/Dropbox $BACKUP
    echo "From ~/GoogleDrive To $BACKUP"
    rsync -a --delete ~/GoogleDrive $BACKUP
    echo "From ~/OneDrive To $BACKUP"
    rsync -a --delete ~/"$ONEDRIVE" $BACKUP
}

backup2(){
    echo "Now copying ~/Library/CELSYS"
    rsync -a --delete ~/Library/CELSYS $BACKUP
}
