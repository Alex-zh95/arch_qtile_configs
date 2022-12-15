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

" Set tab key to produce 4 spaces
set tabstop=4
set expandtab
set shiftwidth=4

" Set automatic indentation
set autoindent
set smartindent

" Allow mouse action
set mouse=a


call plug#begin()

" Nerd-tree file explorer plug-in
"Plug 'preservim/nerdtree'

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

call plug#end()

" Set the color scheme
colorscheme nord

" Navigation shortcuts
nmap <silent> <C-k> :wincmd k<CR>
nmap <silent> <C-j> :wincmd j<CR>
nmap <silent> <C-h> :wincmd h<CR>
nmap <silent> <C-l> :wincmd l<CR>

nmap <silent> <C-a> :wincmd <<CR>
nmap <silent> <C-d> :wincmd ><CR>

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

" Exit Vim if NERDTree is the only window remaining in the only tab.
"autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif

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
