## dotfiles

**build wayland ready system(Arch Linux) with hyprland.**

### Install packages

```
yay -S hyprland warbar-hyprland-git rofi-lbonn-wayland-git \
    swappy swaylock-effects kitty swayidle slurp \
    xdg-desktop-portal-hyprland-git polkit-kde-agent
```

### Install optianal packages

```
yay -S rofi-emoji nwg-look
```

### Install Fonts

```
yay -S ttf-jetbrains-mono-nerd
```

### Stow dotfiles

stow is the dotfiles manager.
git clone the repository to your home.

```
cd dotfiles

stow dunst hypr kitty rofi swappy swaylock waybar environment.d
```

### Wayland known issues

for apps based system electron with blurred interface, use some env variables in `electrons-flags.conf` , and electron build inside the apps should edit `.desktop` files,
add `--enable-features=UseOzonePlatform --ozone-platform=wayland` in `Exec`.

### Theme

[catppuccin](https://github.com/catppuccin/catppuccin)

### wiki

[hyprland](https://wiki.hyprland.org/)
