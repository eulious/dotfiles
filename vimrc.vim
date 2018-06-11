" =============================================================
" ================== Plugin Setting ===========================
" =============================================================
" dein.vim
" http://qiita.com/delphinus/items/00ff2c0ba972c6e41542
let s:dein_dir = expand('~/.vim/dein')
let s:dein_repo_dir = s:dein_dir . '/repos/github.com/Shougo/dein.vim'
if &runtimepath !~# '/dein.vim'
  if !isdirectory(s:dein_repo_dir)
    execute '!git clone https://github.com/Shougo/dein.vim' s:dein_repo_dir
  endif
  execute 'set runtimepath^=' . fnamemodify(s:dein_repo_dir, ':p')
endif
if dein#load_state(s:dein_dir)
  call dein#begin(s:dein_dir)
  let s:toml      = expand('~/Dropbox/.set/vimdein.toml')
  let s:lazy_toml = expand('~/Dropbox/.set/vimdein_lazy.toml')
  call dein#load_toml(s:toml,      {'lazy': 0})
  call dein#load_toml(s:lazy_toml, {'lazy': 1})
  call dein#end()
  call dein#save_state()
endif
if dein#check_install()
  call dein#install()
endif


" neocomplete (公式github設定そのまま)
let g:acp_enableAtStartup = 0
let g:neocomplete#enable_at_startup = 1
let g:neocomplete#enable_smart_case = 1
let g:neocomplete#sources#syntax#min_keyword_length = 3
let g:neocomplete#lock_buffer_name_pattern = '\*ku\*'
let g:neocomplete#sources#dictionary#dictionaries = {
            \ 'default' : '',
            \ 'vimshell' : $HOME.'/.vimshell_hist',
            \ 'scheme' : $HOME.'/.gosh_completions'
            \ }
if !exists('g:neocomplete#keyword_patterns')
    let g:neocomplete#keyword_patterns = {}
endif
let g:neocomplete#keyword_patterns['default'] = '\h\w*'
inoremap <expr><C-g>     neocomplete#undo_completion()
inoremap <expr><C-l>     neocomplete#complete_common_string()
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
    return (pumvisible() ? "\<C-y>" : "" ) . "\<CR>"
endfunction
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"
autocmd FileType css setlocal omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown setlocal omnifunc=htmlcomplete#CompleteTags
autocmd FileType javascript setlocal omnifunc=javascriptcomplete#CompleteJS
autocmd FileType python setlocal omnifunc=pythoncomplete#Complete
autocmd FileType xml setlocal omnifunc=xmlcomplete#CompleteTags
if !exists('g:neocomplete#sources#omni#input_patterns')
    let g:neocomplete#sources#omni#input_patterns = {}
endif
let g:neocomplete#sources#omni#input_patterns.perl = '\h\w*->\h\w*\|\h\w*::'


" neosnippet
"http://kazuph.hateblo.jp/entry/2013/01/19/193745
inoremap <expr><S-TAB>  pumvisible() ? "\<C-p>" : "\<S-TAB>"
imap <silent><C-k> <Esc>:let g:neosnippet_expanding_or_jumpping = 1<CR>a<Plug>(neosnippet_expand_or_jump)
smap <C-k> <Plug>(neosnippet_expand_or_jump)
imap <expr><TAB> pumvisible() ? "\<C-n>" : neosnippet#jumpable() ? "\<Plug>(neosnippet_expand_or_jump)" : "\<TAB>"
smap <expr><TAB> neosnippet#jumpable() ? "\<Plug>(neosnippet_expand_or_jump)" : "\<TAB>"
let g:neosnippet#snippets_directory='~/Dropbox/.set/neosnippet'


" Emmet
let g:user_emmet_expandabbr_key = '<C-e>'
let g:user_emmet_settings = {
            \    'variables': {
            \      'lang': "ja"
            \    },
            \   'indentation': '  '
            \ }


" caw
nmap # <Plug>(caw:hatpos:toggle)
vmap # <Plug>(caw:hatpos:toggle)


" vim-go ( :help vim-go )
let g:go_highlight_extra_types = 1
let g:go_highlight_operators = 1
let g:go_highlight_functions = 1
let g:go_highlight_methods = 1
let g:go_highlight_types = 1
let g:go_highlight_fields = 1
let g:go_highlight_build_constraints = 1
let g:go_highlight_generate_tags = 1
let g:go_highlight_format_strings = 1
let g:go_play_open_browser = 0
let g:go_jump_to_error = 0
let g:go_fmt_autosave = 0
let g:go_doc_keywordprg_enabled = 0
let g:go_def_mapping_enabled = 0
let g:go_gorename_prefill = 0
let g:go_gocode_autobuild = 0
let g:go_gocode_propose_builtins = 0
let g:go_template_autocreate = 0
let g:go_echo_command_info = 0



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

" タブをスベースに
set autoindent
set expandtab
set tabstop=4
set shiftwidth=4
set number

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

" ハイライトとインデント(最後に記述)
syntax on
filetype plugin indent on

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

