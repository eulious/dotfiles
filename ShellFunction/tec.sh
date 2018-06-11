tec(){
    if [ ! -e $1.tex ]; then
        echo "$1.tex is NOT found.";return
    fi
    expect -c "
    set timeout 30
    spawn platex $1.tex 
    expect \"Error\"
    send \"\n\"
    exit 0
    " &> log.txt
    if test `cat $1.log | wc -l` -gt 1; then
        platex $1.tex > /dev/null
        dvipdfmx $1.dvi
        open $1.pdf
    else
        grep ^[!l] log.txt | uniq
        grep line log.txt | uniq
    fi
    rm $1.log
    rm $1.dvi
    rm $1.aux
    rm -f $1.toc
    rm -f $1.nav
    rm -f $1.out
    rm -f $1.snm
    rm log.txt
}
