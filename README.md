# zenFix-Batch-Tool
Python tool (written using ChatGPT) which for now is used to fix oCItem vobs with missing/broken instances. You can also check containers and cross-reference the instances with your scripts.

# How to use
- Make sure you have Python installed
- Run commands `pip install pyfiglet` and `pip install colorama`
- Run `zenFix_main.py`
- Throw UNCOMPILED ZEN into `zenfix_input`
- Use the tool to your needs

# Features
## Scan Broken Instances
Check all broken oCItem blocks in the ZEN file (or files) and store them in `zenfix_instances`.
## Prompt Replacement
Read the broken instances for chosen ZEN (or all) and write replacement for them, then store them in `zenfix_instances`.
## Fix Specific Blocks
Choose specific instance blocks for chosen ZEN (or all) and fix them with the replacements done in Prompt Replacement.
## Fix All Blocks
Fix all instance blocks for chosen ZEN (or all) with the replacements done in Prompt Replacement.
## Batch Fix
Do all the above for every ZEN file in `zenfix_input` in one go.
## Check Containers
Check all containers for chosen ZEN (or all), cross-reference the instances with your scripts and fix the wrong instances. This does not impact amount of items in containers.
## Check Item Validation
Debug function, checks if the app actually has access to the item instances from Daedalus scripts.