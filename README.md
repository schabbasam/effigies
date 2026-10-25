# Effigies

A 3D memory-building game made with Python and Panda3D.

## About

Effigies is a memory game where the player has to memorize a randomly generated block structure and rebuild it from memory.

## Gameplay

1. **Memory phase (20 seconds):** Observe and memorize the generated structure.
2. **Building phase (40 seconds):** Rebuild the structure using blocks of different colors.
3. **Scoring:** Earn points for correct block positions and colors. Incorrect extra blocks reduce your score.

## Features

I tried to structure the code in different classes to make it scalable in the future and make it easier to understand.
This is a minimum viable product, I had a few more features in mind. For example:
- sounds for every action and ambient music
- neat animations for placing and removing blocks
- better UI
- more types of blocks (like stairs, slabs, decorations, even animated fluids and flowers)
- a rotator thing that rotates the hovered block (not relevant for simple cubes)
- a game menu with settings UI and instructions

## Requirements

- Python 3
- Panda3D

## Installation

Clone the repository:

```bash
git clone https://github.com/schabbasam/effigies.git
cd effigies
```

Install Panda3D:

```bash
pip install panda3d
```

## Running the game

```bash
python main.py
```

## Controls

| Action | Control |
|---|---|
| look around | mouse |
| move forward | w |
| move backward | s |
| move left | a |
| move right | d |
| move up | space |
| move down | shift |
| place block | right mouse button |
| remove block | left mouse button |
| change block color | mouse wheel |
| exit | escape |

Note: the movement keybinds are configurable in `user_data.json`.

## Configuration and saves

Game settings and the highscore are stored in `user_data.json`.

## Built with

- Python
- Panda3D

## Resources

I used open source textures from:
- [Basic 3D Shapes Without Texture or Color](https://opengameart.org/content/basic-3d-shapes-without-texture-or-color) for the cube model
- [Kenney's Crosshair Pack](https://kenney-assets.itch.io/crosshair-pack) for the crosshair

A good start to learn using Panda3D is the [official guide and documentation](https://docs.panda3d.org/1.10/python/index).

## License

Everyone is allowed to use this collection of code as long as they mention the author.
