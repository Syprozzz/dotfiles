#!/bin/bash

echo "Updating dotfiles repository from current configs..."

# Top-level dotfiles
cp ~/.bashrc ~/dotfiles/.bashrc
cp ~/.zshrc ~/dotfiles/.zshrc
cp ~/.xinitrc ~/dotfiles/.xinitrc
cp ~/.tmux.conf ~/dotfiles/.tmux.conf
cp ~/.p10k.zsh ~/dotfiles/.p10k.zsh
cp ~/.gitconfig ~/dotfiles/.gitconfig

# Config directories
config_items=(
  btop cava dunst gtk-2.0 gtk-3.0 kitty mpv neofetch
  nvim obsidian pywal qtile ranger rofi spotify systemd wezterm
)

mkdir -p ~/dotfiles/config

for item in "${config_items[@]}"; do
  mkdir -p ~/dotfiles/config/$item
  cp -r ~/.config/$item/* ~/dotfiles/config/$item/ 2>/dev/null
done

echo "Dotfiles updated, You can now commit and push them."
