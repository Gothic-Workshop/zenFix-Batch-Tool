# zenFix-Batch-Tool
zenFix is a powerful batch utility tool (written using ChatGPT in Python) for inspecting and fixing broken or inconsistent data in Gothic .ZEN world files. It automates tedious cleanup tasks, improves modding workflows, and ensures compatibility with in-game mechanics.

# How to use
- Make sure you have Python installed
- Run commands `pip install pyfiglet` and `pip install colorama`
- Run `zenFix_main.py`
- Throw UNCOMPILED ZEN into `zenfix_input`
- Use the tool to your needs

## Config
Other than reading the [game's scripts](https://github.com/VaanaCZ/gothic-2-addon-scripts/tree/Unified-DE/_work/Data/Scripts), zenFix can also convert ZENs between game releases if you have downloaded [GothicZEN](https://forum.worldofplayers.de/forum/threads/1537414-Release-GothicZEN-a-commandline-tool-to-convert-compiled-ZENs-between-Gothic-versions) program first.

Here is an example of `config.xml`:
```xml
<config>
	<scripts src="D:/Gothic Scripts/gothic-2-addon-scripts-Unified-EN/_Work/Data/Scripts/Content/Items" />

	<gothiczen path="D:/Gothic Tools/GothicZEN/GothicZEN.exe" />
</config>
```


# Features
## Scan Broken Instances
Check all broken oCItem blocks in the ZEN file (or files) and store them in `zenfix_instances`.

## Prompt Replacement
Read the broken instances for chosen ZEN (or all) and write replacement for them, then store them in `zenfix_instances`.

## Fix Blocks
Fix instance blocks for chosen ZEN (or all) with the replacements done in Prompt Replacement.

## Batch Fix
Do all the above for every ZEN file in `zenfix_input` in one go.

## Check Containers
Check all containers for chosen ZEN (or all), cross-reference the instances with your scripts and fix the wrong instances. This does not impact amount of items in containers.

## Check Chest Visuals
Check all containers for chosen ZEN to look for chests with mismatched visuals (LOCKED chest for unlocked container and vice versa) or chests which keyInstance or pickLockStr fields are empty, making them unable to be opened.

## Convert ZEN
GothicZEN can convert a compiled ZEN to another Gothic version, or remove LOD polygons when saving to the same version

## Validate Scripts
Debug function, checks if the app actually has access to the item instances from Daedalus scripts.