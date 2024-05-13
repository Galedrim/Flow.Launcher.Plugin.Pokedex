# Flow.Launcher.Plugin.Pokedex

A Flow Launcher plugin to search Pokemon.

Originally create for a French player to retrieve English name of Pokemon and display the most useful information.

There is a LITE version in English

[![GitHub release](https://img.shields.io/github/release/Galedrim/Flow.Launcher.Plugin.Pokedex)]()
[![GitHub latest commit](https://badgen.net/github/last-commit/Galedrim/Flow.Launcher.Plugin.Pokedex)]()
[![Github All Releases](https://img.shields.io/github/downloads/Galedrim/Flow.Launcher.Plugin.Pokedex/total.svg)]()

## Screenshots

#### French Version
![2024-05-13_13-44](https://github.com/Galedrim/Flow.Launcher.Plugin.Pokedex/assets/84284891/7eb9c6a2-6cf2-4d0c-962b-dff81fb98139)

#### English Version
![2024-05-13_13-55](https://github.com/Galedrim/Flow.Launcher.Plugin.Pokedex/assets/84284891/f91da883-fe17-4e39-8dbf-45e125cd13ac)

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
