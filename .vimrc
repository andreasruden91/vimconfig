" Document Structure:
" General Settings
" ...

" General Settings

" Editor Internals
set nocompatible
set history=500
" allow cycling through buffers that contain modifications without appending !
set hidden
" search settings
set incsearch
set ignorecase
set smartcase

" Editor Elements
set ruler
set number

" Format (Whitespace)
set expandtab
set tabstop=4
set softtabstop=4
set shiftwidth=4
set autoindent
set tw=80

" Highlighting & Coloring
syntax on
colorscheme koehler
set background=dark
set hlsearch

" Bindings
" Add some buffer navigation bindings (inspired by tpope's vim-unimpared)
nnoremap <silent> [b :bprevious<CR>
nnoremap <silent> ]b :bnext<CR>
nnoremap <silent> [B :bfirst<CR>
nnoremap <silent> ]B :blast<CR>

" Plugin settings
execute pathogen#infect()
filetype plugin indent on
