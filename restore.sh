#!/bin/bash

echo "Restoring config files to system..."

# Top-level files
cp ~/dotfiles/.bashrc ~/.bashrc
cp ~/dotfiles/.zshrc ~/.zshrc
cp ~/dotfiles/.xinitrc ~/.xinitrc
cp ~/dotfiles/.tmux.conf ~/.tmux.conf
cp ~/dotfiles/.p10k.zsh ~/.p10k.zsh
cp ~/dotfiles/.gitconfig ~/.gitconfig

# Config directories
config_items=(
  btop cava dunst gtk-2.0 gtk-3.0 kitty mpv neofetch
  nvim obsidian pywal qtile ranger rofi spotify systemd wezterm
)

for item in "${config_items[@]}"; do
  mkdir -p ~/.config/$item
  cp -r ~/dotfiles/config/$item/* ~/.config/$item/ 2>/dev/null
done

echo "Dotfiles restored to system config locations."
