# プロンプトを変更
PS1='>>> \W $ '

# 作業ディレクトリの設定
CDPATH=:~/Dropbox

# シェルスクリプト
SHDIR=~/Dropbox/.set/ShellFunction
. $SHDIR/../lib/password.sh
. $SHDIR/tec.sh
. $SHDIR/backup.sh
. $SHDIR/gitinit.sh
. $SHDIR/raspberry.sh
. $SHDIR/../lib/git-completion.bash
. $SHDIR/dl-box.sh
. $SHDIR/paste.sh

# python
PYDIR=~/Dropbox/.set/python
alias hyo='python $PYDIR/hyo.py'
alias todo='python $PYDIR/todo.py'
alias temp='python $PYDIR/temp.py'

# bin
BINDIR=~/Dropbox/.set/bin
alias moji='kotlin -cp $BINDIR/moji.jar MojiKt'
alias kihu='kotlin -cp $BINDIR/kihu.jar KihuKt'
alias igo='kotlin -cp $BINDIR/igo.jar IgoKt &&
    (cd storage/igo/goq;java -jar Goq.jar)'

# エイリアス
alias py='python'
alias vim='env LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/Vim "$@"'
alias doton='defaults write com.apple.finder AppleShowAllFiles TRUE;killall Finder'
alias dotoff='defaults write com.apple.finder AppleShowAllFiles FALSE;killall Finder'
alias so='source ~/.bashrc'
alias o='open .'
alias gita='git add -A;git commit -m `date "+%Y/%m/%d_%H:%M:%S"`'
alias ps='ps | grep -v iTerm | grep -v bash'

# 環境変数
# python
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

# ruby
export PATH="$HOME/.rbenv/bin:$PATH"
if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi

export LD_LIBRARY_PATH=/usr/local/lib

# node.js
export PATH=$HOME/.nodebrew/current/bin:$PATH

# go
export GOPATH=$HOME/GoogleDrive/File/gopath
export PATH=$GOPATH/bin:$PATH
