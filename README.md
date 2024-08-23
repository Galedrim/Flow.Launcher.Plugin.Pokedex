# Flow.Launcher.Plugin.Pokedex

![GitHub release](https://img.shields.io/github/release/Galedrim/Flow.Launcher.Plugin.Pokedex)
![GitHub latest commit](https://badgen.net/github/last-commit/Galedrim/Flow.Launcher.Plugin.Pokedex)
![Github All Releases](https://img.shields.io/github/downloads/Galedrim/Flow.Launcher.Plugin.Pokedex/total.svg)

![image](https://github.com/user-attachments/assets/093a1ad8-2cc1-497c-b01d-a54d544182b3)

## Features

This application provides detailed information on:

- **National Pokémon**
- **Regional Form Pokémon**
- **Mega Evolution**
- **Natures**
- **Abilities**

## Quick Links to Pokémon Resources
Access the following well-known Pokémon websites through the context menu or by clicking on item in the search results:

- [Bulbapedia](https://bulbapedia.bulbagarden.net)
- [Coup Critique](https://www.coupcritique.com)
- [Pokébip](https://www.pokebip.com)
- [Serebii](https://www.serebii.net)
- [Smogon](https://www.smogon.com)

## Requirements

To use Python plugins within Flow-Launcher, you'll need Python 3.11 or later installed on your system. You also may need to select your Python installation directory in the Flow Launcher settings. As of v1.8, Flow Launcher should take care of the installation of Python for you if it is not on your system.

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

Type ```pk``` to start searching in Pokedex.
You can filter Pokemon by typing the name.
