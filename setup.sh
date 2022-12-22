#!/bin/sh

echo "(*) Starting Environment Setup for buttstabber !"
echo "(*) First let's Brew some coffee :-"

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew update
brew upgrade