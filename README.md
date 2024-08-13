# Flow.Launcher.Plugin.Pokedex

![GitHub release](https://img.shields.io/github/release/Galedrim/Flow.Launcher.Plugin.Pokedex)
![GitHub latest commit](https://badgen.net/github/last-commit/Galedrim/Flow.Launcher.Plugin.Pokedex)
![Github All Releases](https://img.shields.io/github/downloads/Galedrim/Flow.Launcher.Plugin.Pokedex/total.svg)

## Features

- Search names of pokémon and their evolutions and display type, abilities and IV information
- Search names of abilities or nature and display effects
- In english, quick access of selected item in [Serebii](https://www.serebii.net/) 
- In french, quick access of selected item in [Pokebip](https://www.pokebip.com)
- Contextual menu with another site : [Smogon](https://www.smogon.com/), [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page), [Coup Critique](https://www.coupcritique.fr/) (French only)

![image](https://github.com/user-attachments/assets/093a1ad8-2cc1-497c-b01d-a54d544182b3)

## Requirements

To use Python plugins within Flow-Launcher, you'll need Python 3.8 or later installed on your system. You also may need to select your Python installation directory in the Flow Launcher settings. As of v1.8, Flow Launcher should take care of the installation of Python for you if it is not on your system.

## Installing

The Plugin has been officially added to the supported list of plugins.
Run the command  ```pm install pokedex``` to install it.

You can also manually add it.

## Manual

Add the plugins folder to %APPDATA%\Roaming\FlowLauncher\Plugins\ and run the Flow command ```restart Flow Launcher```.

## Python Package Requirements

This plugin automatically packs the required packages during release so for regular usage in Flow, no additional actions are needed.

If you would like to manually install the packages:

This plugin depends on the Python flow-launcher package.

Without this package installed in your Python environment, the plugin won't work!

The easiest way to install it is to open a CLI like Powershell, navigate into the plugins folder and run the following command:

``` pip install -r requirements.txt -t ./lib ```

## Usage

Type ```pk``` to start searching Pokedex.
You can filter Pokemon by typing the name.
