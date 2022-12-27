" Enforce vimrc
set nocompatible 

" Add filetype plugin
filetype plugin on

" Enable absolute line numbers 
set number

" Use relative line numbers - absolute will be given on cur line
set relativenumber

" Allow syntax-highlighting
syntax on

" Set encoding
set encoding=UTF-8

" Set tab key to produce 4 spaces
set tabstop=4
set expandtab
set shiftwidth=4

" Set automatic indentation
set autoindent
set smartindent

" Allow mouse action
set mouse=a

" Pane splits
set splitbelow
set splitright

" vsplit with <C-w> <s>, hsplit with <C-w> <v>

" Navigation shortcuts
nmap <silent> <C-k> :wincmd k<CR>
nmap <silent> <C-j> :wincmd j<CR>
nmap <silent> <C-h> :wincmd h<CR>
nmap <silent> <C-l> :wincmd l<CR>

nmap <silent> <C-a> :wincmd <<CR>
nmap <silent> <C-d> :wincmd ><CR>

" Activate horizontal terminal
nmap <silent> <C-x> :term<CR>

call plug#begin()

" Nerd-tree file explorer plug-in
Plug 'preservim/nerdtree'

" Vim dev-icons
Plug 'ryanoasis/vim-devicons'

" Add arline and airlinetheme
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" Add YCM - need to run ./install.py within the plugin folder
Plug 'ycm-core/YouCompleteMe'

" Vimtex plugin for LaTeX in-lining
Plug 'lervag/Vimtex'

" vim-css-color plugin - highlights color on given HEX code
Plug 'ap/vim-css-color'

" Theming Vim to Nord
Plug 'arcticicestudio/nord-vim'

" Vim-wiki
Plug 'vimwiki/vimwiki'

" Enable Jupyter cells in Vim
Plug 'jupyter-vim/jupyter-vim'

call plug#end()

" Set the color scheme
colorscheme nord

" YouCompleteMe (YCM) options
" Enable toggle of diagnostics and completion menu with F3
function Toggle_ycm()
    if g:ycm_show_diagnostics_ui == 0
        let g:ycm_auto_trigger = 1
        let g:ycm_show_diagnostics_ui = 1
        :YcmRestartServer
        :e
        :echo "YCM on"
    elseif g:ycm_show_diagnostics_ui == 1
        let g:ycm_auto_trigger = 0
        let g:ycm_show_diagnostics_ui = 0
        :YcmRestartServer
        :e
        :echo "YCM off"
    endif
endfunction
map <F3> :call Toggle_ycm() <CR>

map <leader>g :YcmCompleter GoToDefinitionElseDeclaration<CR>

" ----- NERDTree settings -----
nnoremap <C-t> :NERDTreeToggle<CR>

" ----- vim-airline theming -----
let g:airline_theme='monochrome'

" ----- VimTex settings -----
let g:tex_flavor='latex'
"let g:vimtex_view_general_viewer='zathura'
"let g:vimtex_quickfix_mode=0

" ----- Vimwiki settings -----
"  Access vim-wiki by <leader>ws (default to \ws)
let wiki_default = {}
let wiki_default.path = '~/Dokumente/vimwiki/'
let wiki_default.syntax = 'markdown'
let wiki_default.ext = '.md'

let wiki_setup = {}
let wiki_setup.path = '~/.setup/wiki/'
let wiki_setup.syntax = 'markdown'
let wiki_setup.ext = '.md'

let g:vimwiki_list = [wiki_default, wiki_setup]

" ----- jupyter-vim settings -----
" Note: Visit https://github.com/jupyter-vim/jupyter-vim for further instructions

" Unset the default keybinds
let g:jupyter_mapkeys = 0

" Set up the Python local leader
let maplocalleader = "-"

" Connecting and disconnecting to Jupyter instance
nnoremap <buffer> <localleader>c :JupyterConnect<CR>
nnoremap <buffer> <localleader>q :JupyterDisconnect<CR>

" Running/importing current file
nnoremap <buffer> <localleader>R :JupyterRunFile<CR>
nnoremap <buffer> <localleader>I :PythonImportThisFile<CR>

" Change to directory of current file
nnoremap <buffer> <localleader>d :JupyterCd %:p:h<CR>

" Send a selection of lines
nnoremap <buffer> <localleader>X :JupyterSendCell<CR>
nnoremap <buffer> <localleader>E :JupyterSendRange<CR>

" Debugging maps
nnoremap <buffer> <localleader>b :PythonSetBreak<CR>
