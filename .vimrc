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

" Exit Vim if NERDTree is the only window remaining in the only tab.
"autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif

" ----- vim-airline theming -----
let g:airline_theme='monochrome'

" Replace standard separators with arrows
"let g:airline_left_sep=''
"let g:airline_right_sep=''

" ----- VimTex settings -----
let g:tex_flavor='latex'
let g:vimtex_view_general_viewer='zathura'
let g:vimtex_quickfix_mode=0
