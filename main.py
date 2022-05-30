import PySimpleGUI as sg
import os.path
import re
import os


class sCFGReader:
    def __init__(self, fileOrString) -> dict:
        # Determine if the fileOrString is a path to a file or the contents of a file
        if os.path.isfile(fileOrString):
            with open(fileOrString, 'r') as f:
                self.configString = f.read()
        else:
            self.configString = fileOrString
        self.config = {}
        return self.convertToDict()

    def export(self, filePath):
        tempString = ""
        # flags
        tabDepth = 0
        inMap = False
        inArena = False
        # Start with the "SpawnConfigs" line
        tempString += "SpawnConfigs\n"
        tempString += "{\n"
        tabDepth += 1
        for mapName in self.config:
            tempString += "\t" * tabDepth
            tempString += "\"" + mapName + "\"\n"
            tempString += "\t" * tabDepth
            tempString += "{\n"
            tabDepth += 1
            for arenaName in self.config[mapName]:
                tempString += "\t" * tabDepth
                tempString += "\"" + arenaName + "\"\n"
                tempString += "\t" * tabDepth
                tempString += "{\n"
                tabDepth += 1
                for key in self.config[mapName][arenaName]:
                    # Skip over the meta_order key
                    if key == "meta_order":
                        continue
                    tempString += "\t" * tabDepth
                    tempString += "\"" + key + "\"\t\t\t"
                    # Type check the value
                    if type(self.config[mapName][arenaName][key]) == str:
                        tempString += "\"" + \
                            self.config[mapName][arenaName][key] + "\"\n"
                    elif type(self.config[mapName][arenaName][key]) == int:
                        tempString += str(self.config[mapName]
                                          [arenaName][key]) + "\n"
                    elif type(self.config[mapName][arenaName][key]) == bool:
                        if self.config[mapName][arenaName][key]:
                            tempString += "\"1\"\n"
                        else:
                            tempString += "\"0\"\n"
                    else:
                        raise Exception("Invalid type")
                tabDepth -= 1
                tempString += "\t" * tabDepth
                tempString += "}\n"
            tabDepth -= 1
            tempString += "\t" * tabDepth
            tempString += "}\n"
        tabDepth -= 1
        tempString += "\t" * tabDepth
        tempString += "}\n"
        with open(filePath, 'w') as f:
            f.write(tempString)

    def convertToDict(self):
        # Convert the config string to a dictionary
        # The format is similar to json, where the key is the first word of the line
        # and the value is the rest of the line
        # values can branch off the key with curly brackets
        # But other than that, no commas or special symbols are allowed
        # except dobule quotes to encapsulate strings

        # First, split the config string into lines
        lines = self.configString.split('\n')
        # Remove comments from all lines, so any text that appears after (and including) a double slah  is removed
        lines = [re.sub(r'//.*', '', line) for line in lines]
        # Remove whitespace or tabs from the beginning of each line
        lines = [line.lstrip() for line in lines]
        # Remove empty lines
        lines = [line for line in lines if line]

        # The first line might contain "SpawnConfigs", if it does, remove it and the next line, and the last line.
        # This way we can handle both the real format and the stupid shit we get from NodeJS
        if lines[0] == "SpawnConfigs":
            lines = lines[2:-1]

        # Some flags
        arenaOrder = 0
        inMap = False
        currentMap = ""
        inArena = False
        currentArena = ""
        # Start a loop through all lines.
        for line in lines:
            # The first layer is the map name, so lets proceed
            if not inMap:
                if line == "{":
                    inMap = True
                    continue
                else:
                    # This regex should match the contents of the quotes
                    match = re.match(r'\"([^\"]+)\"', line)
                    if match:
                        currentMap = match.group(1)
                        self.config[currentMap] = {}
                    else:
                        raise Exception("STINK!")
                    continue
            if inMap:
                if inArena:
                    # If the line is a close bracket, we're done with the current key
                    if line == "}":
                        inArena = False
                        continue
                    # If we're in a bracket, our line will be in the format of "key" "value"
                    # The following regex should capture the key and value
                    match = re.match(r'\"([^\"]+)\"\s+\"([^\"]+)\"', line)
                    # If the regex didn't match, we have a problem
                    if not match:
                        raise Exception("Invalid config format")
                    # If the regex did match, we have the key and value
                    key = match.group(1)
                    value = match.group(2)
                    # Add the key and value to the current dictionary
                    self.config[currentMap][currentArena][key] = value
                    continue
                if line == "{":
                    inArena = True
                    continue
                if ~inArena:
                    # If we aren't in a bracket, we're looking for a key. It will be a string, encapsualted in double quotes
                    # so we need to remove the double quotes
                    if line == "}":
                        inMap = False
                        continue
                    match = re.match(r'\"([^\"]+)\"', line)
                    if match:
                        currentArena = match.group(1)
                        arenaOrder += 1
                        self.config[currentMap][currentArena] = {}
                        self.config[currentMap][currentArena]["meta_order"] = arenaOrder
                    # Add the key to the dictionary
                    continue
        pass

# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("Config"),
        # sg.In(size=(25, 1), enable_events=True, key="-CONFIG-"),
        sg.In(size=(25, 1), enable_events=True, key="-CONFIG-BROWSE-"),
        sg.FileBrowse(button_text="Select Config File",
                      file_types=(("MGEMod Spawn Config", "*.cfg"),),
                      )
    ],
    [
        sg.Text("Map"),
        sg.Combo(values=[], size=(35, 1), enable_events=True, key="-MAPS-"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-ARENA LIST-"
        )
    ],
    [
        sg.Button("Save Config", key="-SAVE-CONFIG-", enable_events=True),
    ]
]

class_column = [
    [
        sg.Text("Allowed Classes",
                tooltip="Classes that can be used in this arena"),
    ],
    [
        sg.Checkbox("Scout", key="scout", enable_events=True),
    ],
    [
        sg.Checkbox("Soldier", key="soldier", enable_events=True),
    ],
    [
        sg.Checkbox("Pyro", key="pyro", enable_events=True),
    ],
    [
        sg.Checkbox("Demoman", key="demoman", enable_events=True),
    ],
    [
        sg.Checkbox("Heavy", key="heavy", enable_events=True),
    ],
    [
        sg.Checkbox("Engineer", key="engineer", enable_events=True),
    ],
    [
        sg.Checkbox("Medic", key="medic", enable_events=True),
    ],
    [
        sg.Checkbox("Sniper", key="sniper", enable_events=True),
    ],
    [
        sg.Checkbox("Spy", key="spy", enable_events=True),
    ],
]


config_editor_column = [
    [sg.Text("Made by Shigbeard", key="-HELP-")],
    [sg.Text("0 Spawnpoints", key="spawncount")],
    [sg.In('', key='arena_name', enable_events=True, size=(25, 1))],
    [
        sg.Text("Arena Type"),
        sg.Combo(values=["ammomod", "mge", "endif"], size=(
            10, 1), enable_events=True, key="arena_type")
    ],
    [
        sg.Text("Frag Limit", tooltip="Frags to win"),
        sg.In('', key="fraglimit", size=(5, 1), enable_events=True),
    ],
    [
        sg.Text("Countdown Time",tooltip="Number of seconds to wait before the player can move after starting"),
        sg.In('', key="cdtime", size=(5, 1), enable_events=True),
    ],
    [
        sg.Text("Min Respawn Distance",tooltip="Minimum distance between players when they spawn"),
        sg.In('', key="mindist", size=(5, 1), enable_events=True),
    ],
    [
        sg.Text("Health Buff", tooltip="Health to set players to after a frag"),
        sg.In('', key="hpratio", size=(5, 1), enable_events=True),
    ],
    [
        sg.Checkbox("Infinite Ammo", key="infammo", enable_events=True, tooltip="If enabled, players will have infinite ammo"),
    ],
    [
        sg.Checkbox("Show Health", key="showhp", enable_events=True, tooltip="If enabled, the enemy player's HP will be always visable on the HUD"),
    ],
    [
        sg.Checkbox("2v2", key="4player", enable_events=True,tooltip="If enabled, this arena will be treated as a 2v2."),
    ],
    [
        sg.Button('Delete', key='-DELETE-', enable_events=True),
        sg.Button('Save', key='save', enable_events=True),
        sg.Button('Reset', key='reset', enable_events=True),
    ],
    # DOESNT WORK
    # [
    #     sg.Button('Modify Spawns', key='-MODIFY-SPAWNS-', enable_events=True),
    # ]
    # DOESNT WORK
]
1
# ----- Full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(config_editor_column, vertical_alignment="top",
                  element_justification="right"),
        sg.Column(class_column, vertical_alignment="top",
                  element_justification="left"),
    ]
]
eventDict = {}


def generate_spawn_row(x):
    r = [sg.Text("", key="{spawnNumber}_SpawnNumber".format(spawnNumber=x)),
         sg.Text("X"),
         sg.In("", key="{spawnNumber}_SpawnX".format(
             spawnNumber=x), size=(10, 1)),
         sg.Text("Y"),
         sg.In("", key="{spawnNumber}_SpawnY".format(
             spawnNumber=x), size=(10, 1)),
         sg.Text("Z"),
         sg.In("", key="{spawnNumber}_SpawnZ".format(
             spawnNumber=x), size=(10, 1)),
         sg.Text("Angle"),
         sg.In("", key="{spawnNumber}_SpawnAngle".format(
             spawnNumber=x), size=(10, 1)),
         sg.Button("Delete", key="{spawnNumber}_DeleteSpawn".format(
             spawnNumber=x), enable_events=True),
         ]
    eventDict["{spawnNumber}_SpawnNumber".format(spawnNumber=x)] = [x]
    eventDict["{spawnNumber}_SpawnX".format(spawnNumber=x)] = [x, "X"]
    eventDict["{spawnNumber}_SpawnY".format(spawnNumber=x)] = [x, "Y"]
    eventDict["{spawnNumber}_SpawnZ".format(spawnNumber=x)] = [x, "Z"]
    eventDict["{spawnNumber}_SpawnAngle".format(spawnNumber=x)] = [x, "Angle"]
    eventDict["{spawnNumber}_DeleteSpawn".format(spawnNumber=x)] = [
        x, "Delete"]
    return r


spawn_controls = [
    sg.Button("Add Spawn", key="AddSpawn", enable_events=True),
    sg.Button("Save Spawns", key="SaveSpawns", enable_events=True),
]

window = sg.Window("Config Viewer", layout)
config = None
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-CONFIG-BROWSE-":
        # Verify that a file was selected
        if values["-CONFIG-BROWSE-"]:
            # Get the file path
            file_path = values["-CONFIG-BROWSE-"]
            # Read the file
            config = sCFGReader(file_path)
            # Get the list of maps
            maps = list(config.config.keys())
            # Update the list of maps
            window["-MAPS-"].update(values=maps, set_to_index=0)
            # Clear the list of Arenas
            # window["-ARENA LIST-"].update(values=[])
            if maps[0] in config.config:
                # Sort the list of arenas by their order
                arena_list = sorted(
                    list(config.config[maps[0]].keys()), key=lambda x: config.config[maps[0]][x]["meta_order"])
                # Update the list of arenas
                window["-ARENA LIST-"].update(values=arena_list)
                # # Get the list of arenas
                # arenas = list(config.config[map_name].keys())
                # # Update the list of arenas
                # window["-ARENA LIST-"].update(values=arenas)
            else:
                # No map selected, clear the list of arenas
                window["-ARENA LIST-"].update(values=[])
        else:
            # No file selected, clear the list of maps
            window["-MAPS-"].update(values=[])
            # Clear the list of Arenas
            window["-ARENA LIST-"].update(values=[])
    if event == "-MAPS-":
        # Get the map name
        map_name = values["-MAPS-"]
        # Make sure there is a key in config.conifg for the map
        if map_name in config.config:
            # Sort the list of arenas by their order
            arena_list = sorted(
                list(config.config[map_name].keys()), key=lambda x: config.config[map_name][x]["meta_order"])
            # Update the list of arenas
            window["-ARENA LIST-"].update(values=arena_list)
            # # Get the list of arenas
            # arenas = list(config.config[map_name].keys())
            # # Update the list of arenas
            # window["-ARENA LIST-"].update(values=arenas)
        else:
            # No map selected, clear the list of arenas
            window["-ARENA LIST-"].update(values=[])
    if event == "-ARENA LIST-":
        # Do nothing if more than one item is selected
        if len(values["-ARENA LIST-"]) == 1:
            missing_values = False
            l_missing_values = []
            # Get the arena name
            arena_name = values["-ARENA LIST-"][0]
            # print(arena_name)
            # Get the arena config
            arena_config = config.config[values["-MAPS-"]][arena_name]
            # Update the image viewer
            window["arena_name"].update(arena_name)
            try:
                window["fraglimit"].update(arena_config["fraglimit"])
            except:
                window["fraglimit"].update("20")
                missing_values = True
                l_missing_values.append("fraglimit")
            try:
                window["cdtime"].update(arena_config["cdtime"])
            except:
                window["cdtime"].update("3")
                missing_values = True
                l_missing_values.append("cdtime")
            try:
                window["mindist"].update(arena_config["mindist"])
            except:
                window["mindist"].update("350")
                missing_values = True
                l_missing_values.append("mindist")
            try:
                window["hpratio"].update(arena_config["hpratio"])
            except:
                window["hpratio"].update("1.5")
                missing_values = True
                l_missing_values.append("hpratio")
            try:
                window["infammo"].update(arena_config["infammo"] == "1")
            except:
                window["infammo"].update(False)
                missing_values = True
                l_missing_values.append("infammo")
            try:
                window["4player"].update(arena_config["4player"] == "1")
            except:
                window["4player"].update(False)
                missing_values = True
                l_missing_values.append("4player")
            try:
                window["showhp"].update(arena_config["showhp"] == "1")
            except:
                window["showhp"].update(False)
                missing_values = True
                l_missing_values.append("showhp")
            try:
                # Find out which arena type is selected
                arena_type = ""
                # Check if the config has either ammomod, mge, or endif keys
                if "ammomod" in arena_config:
                    if arena_config["ammomod"] == "1":
                        arena_type = "ammomod"
                if "mge" in arena_config:
                    if arena_config["mge"] == "1":
                        arena_type = "mge"
                if "endif" in arena_config:
                    if arena_config["endif"] == "1":
                        arena_type = "endif"
                # Update the arena type
                window["arena_type"].update(arena_type)
            except:
                window["arena_type"].update("mge")
                missing_values = True
                l_missing_values.append("arena_type")
            try:
                all_classes = "scout soldier pyro demoman heavy engineer sniper medic spy"
                all_classes_list = all_classes.split(" ")
                classes = arena_config["classes"]
                # split on space
                classes_list = classes.split(" ")
                # Convert our all classes to a dict
                all_classes_dict = {}
                for i in all_classes_list:
                    if i in classes_list:
                        all_classes_dict[i] = True
                    else:
                        all_classes_dict[i] = False
                # Update the class checkboxes
                window["scout"].update(all_classes_dict["scout"])
                window["soldier"].update(all_classes_dict["soldier"])
                window["pyro"].update(all_classes_dict["pyro"])
                window["demoman"].update(all_classes_dict["demoman"])
                window["heavy"].update(all_classes_dict["heavy"])
                window["engineer"].update(all_classes_dict["engineer"])
                window["sniper"].update(all_classes_dict["sniper"])
                window["medic"].update(all_classes_dict["medic"])
                window["spy"].update(all_classes_dict["spy"])
            except:
                classes = "scout soldier pyro demoman heavy engineer sniper medic spy"
                # split on space
                classes_list = classes.split(" ")
                # loop through the list, and tick the checkboxes
                for i in range(len(classes_list)):
                    window[classes_list[i]].update(False)
                missing_values = True
                l_missing_values.append("classes")
            if missing_values:
                window['-HELP-'].update("Loaded some defaults")
            else:
                window['-HELP-'].update("Loaded")
            try:
                x = 0
                print(arena_config)
                for i in range(1, 20):
                    if str(i) in arena_config:
                        x += 1
                window["spawncount"].update(
                    "{spawns} Spawnpoints".format(spawns=str(x)))
            except:
                window["spawncount"].update(
                    "{spawns} Spawnpoints".format(spawns="0"))
    if event == "-DELETE-":
        # Present a confirmation dialog
        yes = sg.popup_yes_no("Are you sure you want to delete this arena?")
        # print(yes)
        if yes == "Yes":
            # Get the map name
            map_name = values["-MAPS-"]
            # Get the arena name
            arena_name = values["-ARENA LIST-"][0]
            # Delete the arena
            del config.config[map_name][arena_name]
            # Update the list of arenas
            window["-ARENA LIST-"].update(
                values=list(config.config[map_name].keys()))
            # Popup a box confirming it's been deleted
            sg.popup("Arena deleted")
        else:
            sg.popup("Arena was NOT deleted")

    if event == "save":
        # Get our values
        arena_cfg = {}
        arena_cfg["fraglimit"] = values["fraglimit"]
        arena_cfg["cdtime"] = values["cdtime"]
        arena_cfg["mindist"] = values["mindist"]
        arena_cfg["hpratio"] = values["hpratio"]
        # Convert from bool to a string
        if values["infammo"]:
            arena_cfg["infammo"] = "1"
        else:
            arena_cfg["infammo"] = "0"
        if values["4player"]:
            arena_cfg["4player"] = "1"
        else:
            arena_cfg["4player"] = "0"
        if values["showhp"]:
            arena_cfg["showhp"] = "1"
        else:
            arena_cfg["showhp"] = "0"
        # For the arena type, the key changes depending on which one is selected
        arena_cfg[values["arena_type"]] = "1"

        # Headache mode
        classes = ""
        if (values['scout']):
            classes += "scout "
        if (values['soldier']):
            classes += "soldier "
        if (values['pyro']):
            classes += "pyro "
        if (values['demoman']):
            classes += "demoman "
        if (values['heavy']):
            classes += "heavy "
        if (values['engineer']):
            classes += "engineer "
        if (values['medic']):
            classes += "medic "
        if (values['sniper']):
            classes += "sniper "
        if (values['spy']):
            classes += "spy "
        # trim trailing whitespace
        classes = classes.rstrip()
        arena_cfg["classes"] = classes
        # Get the map name
        map_name = values["-MAPS-"]
        # Get the arena name
        try:
            arena_name = values["-ARENA LIST-"][0]
        except:
            # Create a popup dialog that warns the user that they need to select an arena
            sg.popup("Please select an arena to save")
            continue
        # Have we changed the name of the arena?
        if arena_name != values["arena_name"]:
            # Verify that the arena name isn't already in use
            if values["arena_name"] in config.config[map_name]:
                # Create a popup dialog that warns the user that the arena name is already in use
                sg.popup("The arena name is already in use")
                continue
            # Create a copy of the arena in the main config
            old_arena = config.config[map_name][arena_name].copy()
            # Delete the old arena
            del config.config[map_name][arena_name]
            # Add the new arena
            config.config[map_name][values["arena_name"]] = old_arena
            arena_name = values["arena_name"]
        # Erase the old arena's area type
        if "ammomod" in config.config[map_name][arena_name]:
            del config.config[map_name][arena_name]["ammomod"]
        if "mge" in config.config[map_name][arena_name]:
            del config.config[map_name][arena_name]["mge"]
        if "endif" in config.config[map_name][arena_name]:
            del config.config[map_name][arena_name]["endif"]
        # Merge the new arena config into the old one
        config.config[map_name][values["arena_name"]].update(arena_cfg)
        # re sort the list of arenas by their order
        arena_list = sorted(
            list(config.config[map_name].keys()), key=lambda x: config.config[map_name][x]["meta_order"])
        # Update the viewer
        window["-ARENA LIST-"].update(
            values=arena_list)
        window["-HELP-"].update("Saved...")
    if event == "reset":
        # Reload the arena
        try:
            arena_config = config.config[values["-MAPS-"]][arena_name]
        except:
            sg.popup("Please select an arena to reset")
            continue

        # Update the image viewer
        window["arena_name"].update(arena_name)
        try:
            window["fraglimit"].update(arena_config["fraglimit"])
        except:
            window["fraglimit"].update("20")
        try:
            window["cdtime"].update(arena_config["cdtime"])
        except:
            window["cdtime"].update("3")
        try:
            window["mindist"].update(arena_config["mindist"])
        except:
            window["mindist"].update("350")
        try:
            window["hpratio"].update(arena_config["hpratio"])
        except:
            window["hpratio"].update("1.5")
        try:
            window["infammo"].update(arena_config["infammo"] == "1")
        except:
            window["infammo"].update(False)
        try:
            window["4player"].update(arena_config["4player"] == "1")
        except:
            window["4player"].update(False)
        try:
            window["showhp"].update(arena_config["showhp"] == "1")
        except:
            window["showhp"].update(False)
        try:
            # Find out which arena type is selected
            arena_type = ""
            if arena_config["arena_type"] == "ammomod":
                arena_type = "ammomod"
            elif arena_config["arena_type"] == "mge":
                arena_type = "mge"
            elif arena_config["arena_type"] == "endif":
                arena_type = "endif"
            # Update the arena type
            window["arena_type"].update(arena_type)
        except:
            window["arena_type"].update("mge")
        try:
            classes = arena_config["classes"]
            # split on space
            classes_list = classes.split(" ")
            # loop through the list, and tick the checkboxes
            for i in range(len(classes_list)):
                window[classes_list[i]].update(True)
        except:
            pass
        try:
            x = 0
            print(arena_config)
            for i in range(1, 20):
                if str(i) in arena_config:
                    x += 1
            window["spawncount"].update(
                "{spawns} Spawnpoints".format(spawns=str(x)))
        except:
            window["spawncount"].update(
                "{spawns} Spawnpoints".format(spawns="0"))
    if event == "-SAVE-CONFIG-":
        # Get the file path to save to
        # file_path = sg.popup_get_file("Save config to...", no_window=True)
        file_path = values['-CONFIG-BROWSE-']
        # If the user didn't cancel
        if file_path != None or file_path != "":
            # Save the config
            config.export(file_path)
            sg.popup("Saved config to {file_path}".format(file_path=file_path),title="Saved")
    if event == "-MODIFY-SPAWNS-":
        # internal screaming
        # get the map and arena
        eventDict = {}
        map_name = values['-MAPS-']
        arena_name = values['-ARENA LIST-'][0]
        haha_funny_list = []
        for i in range(1, 20):
            if str(i) in config.config[map_name][arena_name]:
                haha_funny_list.append(generate_spawn_row(i))
        haha_funny_list.append(spawn_controls)
        llayout = [
            [
                sg.Column(haha_funny_list, vertical_alignment="top",
                          element_justification="center")
            ]
        ]
        wwindow = sg.Window("Spawns", llayout)


window.close()
