set autoindent
set number
set relativenumber
set tabstop=4
set mouse=""
set nocompatible              " be iMproved, required
set incsearch
filetype off                  " required
syntax on

" 启用vundle来管理vim插件
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'altercation/vim-colors-solarized'
Plugin 'tpope/vim-fugitive'
Plugin 'tpope/vim-surround'
Plugin 'chr4/nginx.vim'
Plugin 'stephpy/vim-yaml'
Plugin 'cespare/vim-toml'

call vundle#end()            " required
filetype plugin on    " required
