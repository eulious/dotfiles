# プロンプトを変更
PS1='>>> \W $ '
PROMPT='>>> %c $ '
SETDIR=$HOME/Desktop/config

# 作業ディレクトリの設定
CDPATH=:$HOME/Desktop

# シェルスクリプト
SHDIR=$SETDIR/ShellFunction
. $SHDIR/backup.sh

# python
PYDIR=$SETDIR/python
alias emotion='python $PYDIR/emotion.py'
alias vn='. ./venv/bin/activate'

# bin
BINDIR=$SETDIR/bin

# エイリアス
alias ls='exa'
alias cat='bat'
alias od='hexyl'
alias py='python'
alias doton='defaults write com.apple.finder AppleShowAllFiles TRUE;killall Finder'
alias dotoff='defaults write com.apple.finder AppleShowAllFiles FALSE;killall Finder'
alias so='source ~/.bashrc'
alias o='open .'
alias cot='open -a CotEditor'
u() { uvicorn app:app --port 9000 --reload --reload-dir $1/api; }

# 環境変数
export PATH="/usr/local/sbin:$PATH"
export LANG="ja_JP.UTF-8"
eval $(/opt/homebrew/bin/brew shellenv)

# python
export PATH="$HOME/.pyenv/shims:$PATH"
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

export TFHUB_CACHE_DIR=$HOME/.keras/tfhub
export PYTORCH_ENABLE_MPS_FALLBACK=1
export HF_DATASETS_CACHE="/Volumes/2TB/Library/stable-diffusion"

# node.js
export PATH=$HOME/.nodebrew/current/bin:$PATH

# rust
export PATH=$HOME/.cargo/bin:$PATH

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"