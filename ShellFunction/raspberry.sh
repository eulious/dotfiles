# RaspberryPiの固定IPアドレス
PIIP=192.168.2.224

# RaspberryPiにログイン
pi(){
    ssh pi@$PIIP
}

# SSHでコピー
picp(){
    expect -c "
    spawn env LANG=C /usr/bin/scp $1 pi@$PIIP:~/$2
    expect \"password:\"
    send \"rasp\n\"
    interact
    "
    # scp -r $1 pi@$PIIP:scp/$2
}


# SSHで同期
pirs(){
    echo "Syncing from Mac to RaspberryPi"
    # rsync -auv ~/Dropbox/prog/rasp pi@$PIIP:/home/pi/
    rsync -auv ~/Dropbox/prog/rasp pi@$PIIP:/home/pi/Dropbox/
    rsync -auv ~/Dropbox/.set pi@$PIIP:/home/pi/Dropbox/
    echo "Syncing from RaspberryPi to Mac"
    rsync -auv pi@$PIIP:/home/pi/Dropbox/rasp ~/Dropbox/prog/
}

<<COMMENT
# 以前のPIIP取得方法
PIIP=`grep OFFER /var/log/system.log \
    | sed -n '$p' \
    | sed -e "s/.*192/192/g" \
    | sed -e "s/\ .*//g"`
COMMENT
