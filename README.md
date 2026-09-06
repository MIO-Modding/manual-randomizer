# MIO: Memories in Orbit -- Manual Randomizer
This project serves as a placeholder for a randomizer mod implementing Archipelago support for MIO: Memories in Orbit. The primary goals of this randomizer are to get a glimpse of how awesome a MIO randomizer will be, and to begin proofing logic while the mod support is being developed.

To that end, this is not a fully polished perfect randomizer, and bugs are likely to abound. Please report anything you find amiss be it in logic or in your adventuring!

### What's a Manual Randomizer?
See the upstream Manual documentation for details, but broadly speaking a manual randomizer is a way for you to be the interface between a game you want to randomizer (MIO) and Archipelago. This is as opposed to a regular randomizer where the monkeys in the computer are the interface instead. 

## Playing the (a) Manual
Download `manual_mio_samwell.apworld` from the latest releases and install it into your Archipelago client (don't rename this file). It's also recommended to install the latest version of Universal Tracker. Use Archipelago's built in `Options Creator` tool to create a yaml, and generate and host an Archipelago seed like any other Archipelago (or ask your host to).

To connect to and play the game, you may use the generic Manual client described here or you can use the [Interactive Map](https://mio-modding.github.io/interactive-map/). We describe the manual client in the rest of this section, though the map is likely to be the better fit for most MIO players.

### Using the generic Manual Client
Once the room is being hosted, you can connect to it using the `Manual Client` tool which is installed into Archipelago by having a Manual randomizer apworld (like `manual_mio_samwell.apworld`). If you have multiple manual randomizers installed you may need to change the game you have selected in the `Manual Game ID` dropdown near the top, afterwhich you can connect to Archipelago like in other text clients by putting the relevant `ip:port` in the textbox at the very top, clicking connect, and typing your slot name into the command prompt (at the bottom of the client) when prompted.

You can send checks by changing to the `Manual` tab (under the `Manual Game ID` dropdown). If you are connected you should see two columns of collapsable categories. On the right are locations you can visit in your world and on the left are items you or others can find for your world. If you installed Universal tracker then regions with locations (on the right) which are in logic will be highlighted green and clicking on a green location will tell Archipelago to send whatever item randomized to that location to the player to whom that item belongs. On the other hand, as you are sent items they will appear in the dropdowns on the left of the screen. Your most recent item received is bolded, and will appear in the relevant categories in the order they are recieved (most recent at the bottom of a category). Because only the most recent item is bolded, it's recommended to monitor the console log in the `Archipelago` tab of the client, or open a second client to better notice when you are given items.

## Playing the (this) Manual
Instead of using the generic manual client, you may (and are recommended to) use the [Interactive Map](https://mio-modding.github.io/interactive-map/). This full feature client will show you available checks, incoming items, and allow you to send items. For more info see the cooresponding forum post in the MIO discord or on the [github for the map](https://github.com/MIO-Modding/interactive-map). 

Beyond running a manual client, your job is also to give yourself the items sent to you from the multiworld. Ultimately this boils down to using the developer debug menu to give yourself the relevant items. Below we outline some guidlines on using debug, as well as how we recommend managing your items so as to maximize gameplay over clicking things in the menu.

### Enabling debug
Enabling the developers' debug menu consists of adding a file to your MIO installation, and activating it once the game has started up. You need a controller with a d-pad input to enable debug. You cannot activate debug with only a keyboard. 

-1 Download the file `VERY_SECRET_DO_NOT_OPEN` (available in the pinned messages of the `general-datamining` channel on the MIO discord) and place it in your MIO install folder. If you installed your game through steam you can locate this folder by selecting `Manage > Browse Local Files` under the gear icon on the game's library page. In general you are looking for the folder with `mio.exe` (not a shortcut to `mio.exe`).

-2 With the file installed, boot up MIO. On the title screen use your d-pad to input the following: `Up, Down, Up, Down, Left, Right, Left, Right, Down, Left, Up, Right`. If done correctly you should see various text appear on screen. Congrats! You've enabled debug.

### Using debug
With debug enabled you can press `F11` at any time to open the debug menu. If you are in game you can modify save flags (which you will do a lot), toggle various debug states such as displaying collisions (which can be useful for learning/practicing skips), infinite energy, hairpinning to anything, invincibility, and so on. If this is your first time using debug, play around with it for a bit and have some fun.

Of particular interest for the manual randomizer is the `Save Editor`. From here you may add or remove items from your current save file. Changes are reflected immediately in game (some things may require a room to be reloaded). For example, if you are sent the item `TRINKET>HOOK_BERSERKER (Modifier - Wild Cat)`, you would open the debug menu with `F11`, under the `Save Editor` dropdown open the `TRINKET` dropdown, and check the box that says `HOOK_BERSERKER`. Close the debug menu with `F11` and you should now see in your modier inventory that you have Wild Cat. Items in the manual are grouped the same way they are in the save editor, and named with the relevant save flag, followed by the regular name you would see in game.

Another useful option you may choose to enable is to show Zone names and ids, which is located at the very bottom of the debug menu. This can make it easier to find a room listed as having an item in logic, though you can always see what room you are in using the text in the bottom left corner of the screen. 

Lastly, if for some reason you need to return to your starting location (which is permitted and sometimes expected in Archipelago logic) or escape a softlock, you can enable noclip/teleport by clicking the left stick on your controller. Clicking the left stick again exits this mode.

### Setting up your save
There are a few flags which should be adjusted in a fresh save file in order for the manual logic to function properly. These changes should be made before properly starting the randomizer.
- Remove `TRINKETS > HUD` to remove the self awareness modifier. The game appears to re-add `TRINKETS > HUD` to your inventory every time you load your save. You may choose instead to abstain from using it if you find removing it tedious.
- If you randomized slash, remove `UPGRADE > SLASH` in the save editor. Notably, the game sets this flag to true when you complete the intro sequence, so this must be done after Mio wakes up.
- Capucine moving around is difficult to control, so we recommend immediately placing Capucine in her House state. `PLOTPOINTS > CAPU > QUEST: HOUSE`
- If your starting location is not the scrapyard (default, and the only option currently) then you need to teleport to the proper starting location once Mio wakes up.

### Guidelines on using debug for the Manual
In an ideal randomizer you would immediately get every item sent to you from the multiworld. In this manual that is ill advised for two primary reasons.

Firstly, using the debug menu for every flag takes time away from gameplay. If you are playing in a multiworld with others you may be sent an item every few seconds at times, and waiting until you're sent an item you actually need can save time to help you continue sending items back.

Secondly, and perhaps more importantly, MIO uses the same flags for deciding whether an item should appear on the ground as it does for deciding whether you have an item. This means that once you give yourself an item sent by the multiworld, it will no longer appear in your game. You should send the check for a location when you are standing where it should be regardless of whether it is visible in game or not. Waiting to give yourself items you don't immediately need may make it easier to find their corresponding locations in game.

You can always see all of the items you have recieved using the manual client, so it may be beneficial to not give yourself old cores, keys, candles or other items until you have enough to need them or are at a place you can use them. Alternatively, you could choose to collect these items as you check their vanilla locations and "manually" restrict yourself from using them in game unless the tracker shows you having them in their proper amounts. Similarly, many items such as Traveller Logs, Flash Memories, Pearl Orders, and so on do nothing to change logic and may be collected or not collected at any time without impacting the randomizer experience.

### Deathlink
If you enabled deathlink, the meaning should be fairly evident. If you die in game, click the `Death Link: Primed` button in the top corner of your tracker. Note that in general this button should be grey. When you send a deathlink the button will turn green and say `Death Link: Sent`. Clicking it again will return it to the primed state. If it is red, someone else has sent you a death link and you should die in game. You can do that either by jumping into enemies/hazards until you run out of health, or in the debug menu there is a `kill mio` checkbox under the `combat debug` tab.

## Building the Manual
If you wish to build the Manual yourself (for example, if you'd like to modify it to meet your own needs or contribute) you may either do it "manually" or use the included `setup.sh` and `build.sh` scripts (a windows `.bat` version of these files might be appreciated).

### Manually building
The steps to build this manual are essentially the same as for any other manual Archipelago.

-1 Download a current release of a manual randomizer. For this you may use a release directly from the upstream Manual repository (`manual_stable_yyyymmdd.apworld`), or you may use a current release of `manual_mio_samwell.apworld`. Any file with the `.apworld` extension is actually a `.zip` file. Unzip your release either by associating the `.apworld` file extension with zipped archives, or by renaming your `.apworld` file to end in `.zip` instead. This should extract a single folder. Rename this extracted folder to `manual_mio_samwell`. Do not change this name unless you are making substantial changes to the structure of the manual in which case you should also update the info in `fixed_data/game.json`.

-2 Run `python tomo.py`. Optionally, you may add a custom path to `world.json` as a first argument (defaults to `<project_dir>/world.json`) and a custom destination for the output files (defaults to `<project_dir>/manual_mio_samwell/data`). This will parse `world.json` (provided with the upstream `mio.apworld` and this repository) and produce `items.json`, `locations.json`, `regions.json` and `events.json` in the output directory. This will overwrite previous versions of these files in the output directory.

-3 Copy all files from `static_inputs` into `manual_mio_samwell`. The files in `static_inputs` are not changed by `tomo.py` and therefore do not need to be updated when `world.json` is updated. Note that in `static_inputs/hooks` only `Options.py` and `World.py` currently have any significant deviations from the tempate files distributed with manual. The others are provided for completeness.

-4 Zip `manual_mio_samwell` into a zip archive and rename it to `manual_mio_samwell.apworld`. Note that the contents of this archive should include the `manual_mio_samwell` folder, not just the files inside.

-5 Install and use this `manual_mio_samwell.apworld` as you would any other apworld. 

### Using the scripts
There are two small scripts included to help streamline the build process. Note they are currently only provided as bash scripts. To build the apworld using the scripts, do the following.

-1 Download a current release of a manual randomizer. For this you may use a release directly from the upstream Manual repository (`manual_stable_yyyymmdd.apworld`), or you may use a current release of `manual_mio_samwell.apworld`. From the root of this project, run 
```bash
  ./setup.sh <path to your manual.apworld>
```
which will unzip the apworld and rename it to `manual_mio_samwell`. This step only needs to be done once.

-2 From the root of this project run `./build.sh`. This will run `tomo.py`, copy the files from `static_inputs` into `manual_mio_samwell/data` and zip the instance into `manual_mio_samwell.apworld`. Optionally you may provide a path to your Archipelago worlds folder (for Linux `./build.sh ~/.local/share/Archipelago/worlds`) and the script will copy the zipped `manual_mio_samwell.apworld` directly to your Archipelago installation.


