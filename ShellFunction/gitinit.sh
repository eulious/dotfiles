gitinit(){
    git init
    cp ~/dropbox/.set/ShellFunction/.gitignore .
    vim .gitignore
    git add .
    git commit -a -m"Initial Commit"
}
