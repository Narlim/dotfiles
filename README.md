## dotfiles

**build wayland ready system(Arch Linux) with hyprland.**

Reference Project:
[https://github.com/iamverysimp1e/dots](https://github.com/iamverysimp1e/dots)

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

### Ranger kitty picture preview
```
stow ranger
yay -S python-pillow
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

- for apps based system electron with blurred interface, use some env variables in `electrons-flags.conf` , and electron build inside the apps should edit `.desktop` files,
  add `--enable-features=UseOzonePlatform --ozone-platform=wayland` in `Exec`.

- for some qt apps like may have scaling problem, the `QT_AUTO_SCREEN_SCALE_FACTOR=0,QT_SCALE_FACTOR=1.5` is useful. The env variables can make telegram GUI too big, use the `Exec=env -u QT_SCALE_FACTOR /usr/bin/telegram-desktop -- %u` to avoid it.

### Theme

[catppuccin](https://github.com/catppuccin/catppuccin)

### wiki

[hyprland](https://wiki.hyprland.org/)
