## dotfiles

build wayland ready system(Arch Linux) with hyprland.

### Install packages

```
yay -S hyprland warbar-hyprland-git rofi-lbonn-wayland-git swappy swaylock-effects kitty
```

### Stow dotfiles

git clone the repository to your home
```
cd dotfiles

stow dunst hypr kitty rofi swappy swaylock waybar environment.d
```
