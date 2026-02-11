# zenFix-Batch-Tool

`zenFix` is a batch utility for inspecting and fixing broken or inconsistent data in Gothic `.ZEN` world files.
It helps with routine modding cleanup: scanning invalid item instances, preparing replacements, applying fixes, validating containers, and converting ZEN files between game versions.

## Requirements

- Python 3.10+ recommended
- Dependencies:
  - `pyfiglet`
  - `colorama`

Install dependencies:

```bash
pip install pyfiglet colorama
```

## Quick start

1. Run `python zenFix_main.py`.
2. Put **uncompiled** `.ZEN` files into `zenfix_input`.
3. Use the menu options to scan, generate replacements, and apply fixes.
4. Collect outputs from `zenfix_output` and generated fix/list files from `zenfix_instances`.

## Generated folders

The tool auto-creates these folders on startup:

- `zenfix_input` – source ZEN files
- `zenfix_output` – processed and converted output files
- `zenfix_instances` – broken instance lists and replacement maps
- `zenfix_broken` – auxiliary files for broken data workflows
- `zenfix_log` – action logs

## Feature overview (all menu actions)

### Info and setup

- **About**
  - Shows project information and repository link.
- **Validate Scripts**
  - Debug/helper action to confirm script path loading and how many valid item instances are currently available.

### Instance discovery and replacement mapping

- **Scan Broken Instances (single ZEN / all ZENs)**
  - Scans `oCItem` blocks and writes broken instance names into `*_instanceList.txt` files in `zenfix_instances`.
- **Prompt Replacements (single list / all lists)**
  - Opens previously generated `*_instanceList.txt`, asks for replacements, and writes `*_instanceFix.txt` maps.

### Fixing workflows

- **Fix Specific Instance (single ZEN / all ZENs)**
  - Applies one chosen replacement entry from fix maps.
- **Fix All Blocks (single ZEN / all ZENs)**
  - Applies all replacements from available `*_instanceFix.txt` files.
- **Batch Fix**
  - End-to-end flow: scans all ZENs, prompts replacements for all found broken instances, then applies fixes across files.

### Container and visual validation

- **Check Containers (single ZEN / all ZENs)**
  - Validates `contains=string:` entries, cross-checks instances against loaded scripts, prompts fixes, and rewrites corrected files.
- **Check Chest Visuals**
  - Detects chest visual/lock mismatches and missing lock/key data that can make containers unopenable.
- **Count zCVob Visual Usage**
  - Counts `zCVob` `visual=string:` usage where `showVisual=1`, with optional visual-name filtering, and writes a report to `zenfix_output`.

### Conversion

- **Convert ZEN between Gothic versions**
  - Uses GothicZEN to convert compiled ZEN files between Gothic versions.

## Config (`config.xml`)

The tool reads paths from `config.xml`:

- `scripts src="..."` for Daedalus script item validation.
- `gothiczen path="..."` for ZEN conversion support.

Example:

```xml
<config>
    <scripts src="D:/Gothic Scripts/gothic-2-addon-scripts-Unified-EN/_Work/Data/Scripts/Content/Items" />

    <gothiczen path="D:/Gothic Tools/GothicZEN/GothicZEN.exe" />
</config>
```

## Typical usage order (recommended)

1. **Scan Broken Instances (all ZENs)**
2. **Prompt Replacements (all lists)**
3. **Fix All Blocks (all ZENs)**
4. Optional: run **Check Containers** and **Check Chest Visuals**
5. Optional: run **Count zCVob Visual Usage** for visual audits

If you prefer one-click processing, use **Batch Fix**.
