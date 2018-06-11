#!/bin/bash

DLBOX=192.168.54.218
MYBOX=~/"$ONEDRIVE"/研究室
alias dl='sshrc dl-box@$DLBOX'

dl2tn(){
    rsync -av --delete dl-box@$DLBOX:~/.takeuchi/* "$MYBOX"/dl-box \
        --exclude='dat/*' \
        --exclude='out/*' \
        --exclude='etc/*'
}

tn2dl(){
    expect -c "
    spawn env LANG=C /usr/bin/scp $1 dl-box@$DLBOX:~/.takeuchi/$2
    expect \"password:\"
    send \"${DLBOXPW}\n\"
    interact
    "
}
