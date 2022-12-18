" =============================================================
" ================== Basic Settings ===========================
" =============================================================

" CUIのテーマを設定する(最初に記述)
let g:hybrid_use_iTerm_colors = 1
colorscheme desert

" カレント行ハイライト
set cursorline
highlight CursorLine cterm=underline ctermfg=NONE ctermbg=NONE
highlight CursorLine gui=underline guifg=NONE guibg=NONE

augroup HilightsForce
  autocmd!
  autocmd WinEnter,BufRead,BufNew,Syntax * :silent!
              \  call matchadd('Todo', '\(TODO\|NOTE\|INFO\|XXX\|TEMP\)')
  autocmd WinEnter,BufRead,BufNew,Syntax * highlight Todo guibg=Red guifg=White
augroup END


" タブをスベースに
set autoindent
set expandtab
set tabstop=4
set shiftwidth=4

" バックアッブしない
set noswapfile
set nobackup
set noundofile

" Emacsキーバインド
imap <C-a>  <Home>
imap <C-b>  <Left>
imap <C-f>  <Right>

" クリッブボードを連携する
set clipboard=unnamed

" 論理行移動→物理行移動
nnoremap j gj
nnoremap k gk
vnoremap j gj
vnoremap k gk

" 変更中のファイルでも、保存しないで他のファイルを表示する
set hidden

" 外部でファイルに変更がされた場合は読みなおす
set autoread   

" マウスの入力を受け付ける
set mouse=a

" 行番号を表示する
set number

" ステータスラインを常に表示
set laststatus=2
set ruler

" 勝手な改行を阻止
set formatoptions=q

" 検索関係
set incsearch
set hlsearch 

" '<'や'>'でインデントする際に'shiftwidth'の倍数に丸める
set shiftround

" 対応括弧に'<'と'>'のペアを追加
set matchpairs& matchpairs+=<:>

" vを二回で行末まで選択
vnoremap v $h

" ビープ音を無効
set visualbell t_vb=

" ESCキーをC-jに変更
noremap <C-j> <esc>
noremap! <C-j> <esc>

" 挿入モードを抜けたときにIMEオフ(MacVim限定)
" http://qiita.com/komapotter/items/2cc899b0e95806b29fc7
if has('gui_macvim')
    set imdisable
endif

" 括弧の補完
inoremap {<Enter> {}<Left><CR><ESC><S-o>
inoremap [<Enter> []<Left><CR><ESC><S-o>
inoremap (<Enter> ()<Left><CR><ESC><S-o>

" =============================================================
" ================== FileType Settings ========================
" =============================================================

" ハイライト
autocmd FileType go :highlight goErr cterm=bold ctermfg=214
autocmd FileType go :match goErr /\<err\>/

if (expand("%:e") == "py")
    syn keyword Function self
endif


" ハイライトとインデント(最後に記述)
syntax on
filetype plugin indent on


" TXT
if (expand("%:e") == "txt")
    filetype plugin indent off
    let g:neocomplete#enable_at_startup = 0
    iunmap {<Enter>
    iunmap [<Enter>
    iunmap (<Enter>
endif

" Latex
if (expand("%:e") == "tex")
    let g:neocomplete#enable_at_startup = 0
    set tabstop=1
    set shiftwidth=1
    iunmap {<Enter>
    iunmap [<Enter>
    iunmap (<Enter>
endif

" インデント幅を２にする言語
if (expand("%:e") == "rb") ||
            \ (expand("%:e") == "html") ||
            \ (expand("%:e") == "scale") ||
            \ (expand("%:e") == "php")
    set tabstop=2
    set shiftwidth=2
endif

" タブを使用する言語
if (expand("%") == "Makefile") ||
            \ (expand("%") == "makefile") ||
            \ (expand("%:e") == "go") ||
            \ (expand("%:e") == "snip")
    set noexpandtab
endif

" HtmlとPHP以外はEmmetを無効"
if expand("%:e") != "html"
    if expand("%:e") != "php"
        imap <C-e>  <End>
    endif
endif
