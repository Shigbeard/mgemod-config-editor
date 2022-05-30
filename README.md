# MGEMod Config Viewer

This tool allows for effortless modification of an existing MGEMod Spawn Config, using PySimpleGUI.

## Requirements

- [Python >=3.10](https://www.python.org/downloads/)
- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)
- An existing .cfg file for [MGEMod](https://github.com/sapphonie/MGEMod)

## Usage

1. Open the script in your terminal of choice: `python main.py`
![](https://i.imgur.com/GP7vw3b.png)
2. Click on `Select Config File` and open a config file for MGEMod
![](https://i.imgur.com/mu5tq4Y.png)
3. Once loaded, the first map in your config will automatically be selected, and the arenas for it will appear in the list below. Select the arena you wish to modify, or the map you wish to modify.
![](https://i.imgur.com/DvZMcoT.png)
4. Once an arena is selected, the configs for that arena (or the defaults) will load on the right. Fill in your desired settings, and then click `Save` to save that arena in memory.
![](https://i.imgur.com/GTaFvIH.png)
5. When satisfied, save the config file by clicking `Save Config`.

## Known Issues

- The config file is not saved to disk until you click `Save Config`.

    - This is intentional behavior, to prevent accidental data corruption.

- It isn't possible to modify spawn coordinates

    - While they do save, they cannot be modified with this tool. Mainly because I haven't developed a module to do so yet. And I likely wont.

- Not all MGE options are listed, or respected by this tool.

    - A lot of MGE features are simply unused by the wider community in my experience. Very few people play ultiduo, koth or bball in MGE, and dedicated bball maps already exist. If people genuinely wanted to play ultiduo or koth, they'd book a Qix server.

## Potential Issues (aka I didn't test these things)

- Complex Configs
    
    - I've only been testing against single map configs spat out by this tool or by [pepperkick's ChillyMGE scripts](https://github.com/pepperkick/ChillyMGE/tree/master/scripts). While theoretically it should be able to trim out comments, blank spaces, and poorly formatted live configs, I haven't tested this.

- Bad Configs

    - I've only got limited data format verification in place. I'm not really good at writing parsers, and I'm lucky that the Sourcemod configuration is really really basic.

## Contributing

If you wanna contribute to this project, by all means. GPL 3.0 applies, whatever that means.