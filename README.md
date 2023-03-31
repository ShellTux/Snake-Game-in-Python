# Snake Game

A classic snake game written in Python using Pygame.

## Game Overview

In this game, the player controls a snake that moves around the screen.
The snake must eat food items to grow longer and increase its score.
The game ends if the snake collides with a wall or its own body.

![Snake Game](images/snake.gif)

## Prerequisites

- Python 3.x
- Tkinter

## Installing

Clone the repo using

```zsh
git clone https://github.com/ShellTux/Snake-Game-in-Python.git
```

Install tkinter using pip

```zsh
pip3 install tkinter
```

This might not be sufficient to run on your linux machine,
so install tkinter through your linux distro package manager.

### Debian/Ubuntu

```zsh
sudo apt-get install python3-tk
```

### CentOS/RHEL

```zsh
sudo yum install python3-tkinter
```

### Fedora

```zsh
sudo dnf install python3-tkinter
```

### Arch Linux

```zsh
sudo pacman -S tk
```

### OpenSUSE

```zsh
sudo zypper install python3-tk
```

Note that the package name may differ based on the specific
version of the distribution and the package manager being used.

## How to Play

- Run the game using

```zsh
python main.py
```

or

```zsh
python3 main.py
```

or

```zsh
./main.py
```

make sure the script has executable permissions.

- Use the arrow keys to control the snake's movement.
- Eat the food items to grow longer and increase your score.
- Avoid colliding with walls or your own body.

## Acknowledgments

Inspired by classic snake games from the past.
Thanks to Pygame for providing an easy-to-use library for game development in Python.
