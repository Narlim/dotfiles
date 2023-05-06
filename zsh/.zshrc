# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
# if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
#   source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
# fi

### Added by Zinit's installer
if [[ ! -f $HOME/.local/share/zinit/zinit.git/zinit.zsh ]]; then
    print -P "%F{33} %F{220}Installing %F{33}ZDHARMA-CONTINUUM%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
    command mkdir -p "$HOME/.local/share/zinit" && command chmod g-rwX "$HOME/.local/share/zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.local/share/zinit/zinit.git" && \
        print -P "%F{33} %F{34}Installation successful.%f%b" || \
        print -P "%F{160} The clone has failed.%f%b"
fi

source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# 主题
# zinit ice compile'(pure|async).zsh' pick'async.zsh' src'pure.zsh'
# zinit light sindresorhus/pure
zinit ice depth=1
zinit light romkatv/powerlevel10k

# 语法高亮
zinit ice lucid wait='0' atinit='zpcompinit'
zinit light zdharma-continuum/fast-syntax-highlighting

# 自动建议
zinit ice lucid wait="0" atload='_zsh_autosuggest_start'
zinit light zsh-users/zsh-autosuggestions

# 补全
zinit ice lucid wait='0'
zinit light zsh-users/zsh-completions

# 加载 OMZ 框架及部分插件
zinit snippet OMZ::lib/completion.zsh
zinit snippet OMZ::lib/history.zsh
zinit snippet OMZ::lib/theme-and-appearance.zsh
# zinit snippet OMZ::plugins/autojump/autojump.plugin.zsh
zinit snippet OMZ::plugins/command-not-found/command-not-found.plugin.zsh

zinit load djui/alias-tips

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

alias cd1="cd .."
alias cd2="cd ../.."
alias cd3="cd ../../.."
alias cd4="cd ../../../.."
alias cd5="cd ../../../../.."

function mkdircd () { mkdir -p "$@" && eval cd "\"\$$#\""; }

# source /usr/share/nvm/init-nvm.sh

# env
export SYSTEMD_LESS=FRXMK

# pyenv
export PATH="${HOME}/.pyenv/shims:${HOME}/.local/bin:${PATH}"
eval "$(pyenv init -)"

# http_proxy
export HTTP_PROXY="http://127.0.0.1:8118/"
export HTTPS_PROXY="http://127.0.0.1:8118/"
