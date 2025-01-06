# プロンプトを変更
PS1='>>> \W $ '
PROMPT='>>> %c $ '
CDPATH=:$HOME/Nextcloud/hiro/www

# エイリアス
alias vn='. ./venv/bin/activate'
alias py='python'
alias doton='defaults write com.apple.finder AppleShowAllFiles TRUE;killall Finder'
alias dotoff='defaults write com.apple.finder AppleShowAllFiles FALSE;killall Finder'
alias so='source ~/.zshrc'
alias o='open .'
u() { uvicorn app:app --port 9000 --reload --reload-dir $1/api; }

# 環境変数
export PATH="/usr/local/sbin:$PATH"
export LANG="ja_JP.UTF-8"
eval $(/opt/homebrew/bin/brew shellenv)

# python
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PATH="$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH"
eval "$(pyenv init -)"

# rust
export PATH=$HOME/.cargo/bin:$PATH

# java
export PATH="/usr/local/opt/openjdk/bin:$PATH"
export CPPFLAGS="-I/usr/local/opt/openjdk/include"

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# backup
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
