# zenFix-Batch-Tool

`zenFix` is a batch utility for inspecting and fixing broken or inconsistent data in Gothic `.ZEN` world files.
It helps with routine modding cleanup: scanning invalid item instances, preparing replacements, applying fixes, validating containers, and converting ZEN files between game versions.

## Requirements

- Python 3.11+ recommended (uses built-in `tomllib`)
- Dependencies:
  - `pyfiglet`
  - `colorama`

Install dependencies:

```bash
pip install pyfiglet colorama
```

## Quick start

1. Run `python zenFix_main.py`.
2. Put **uncompiled** `.ZEN` files into `zenFix_Input` (or change `[directories].input` in `config.toml`).
3. Use the menu options to scan, generate replacements, and apply fixes.
4. Collect outputs from `zenFix_Output` and generated fix/list files from `zenFix_Instances` (or use your configured directories).

## Generated folders

The tool auto-creates these folders on startup:

- `zenFix_Input` ? source ZEN files
- `zenFix_Output` ? processed and converted output files
- `zenFix_Instances` ? broken instance lists and replacement maps
- `zenFix_Broken` ? auxiliary files for broken data workflows
- `zenFix_Log` ? action logs

## Feature overview (all menu actions)

### Info and setup

- **About**
  - Shows project information and repository link.
- **Validate Scripts**
  - Debug/helper action to confirm script path loading and how many valid item instances are currently available.

### Instance discovery and replacement mapping

- **Scan Broken Instances (single ZEN / all ZENs)**
  - Scans `oCItem` blocks and writes broken instance names into `*_instanceList.txt` files in the configured instances directory.
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
- **Check oCMOB focusName**
  - Validates `focusName=string:` values in `oCMOB` blocks against loaded script tokens and writes a report to the configured output directory.
  - Optional repeat-family check flags variants such as `MOBNAME_GRAVE*` (e.g. `MOBNAME_GRAVE`, `MOBNAME_GRAVE_01`, `MOBNAME_GRAVEA`).
- **Check MOBNAME duplicates by configured prefixes (all ZENs)**
  - Scans all input ZENs for duplicated `focusName` values that start with configured prefixes from `config.toml` (`[focus].name_prefixes`).
  - Writes a consolidated report to `<output>/FocusNamePrefixDuplicatesReport.txt`.
- **Count zCVob Visual Usage**
  - Counts `zCVob` `visual=string:` usage where `showVisual=1`, with optional visual-name filtering, and writes a report to the configured output directory.

### Conversion

- **Convert ZEN between Gothic versions**
  - Uses GothicZEN to convert compiled ZEN files between Gothic versions.

## Config (`config.toml`)

The tool now uses a layered TOML configuration with defaults and optional feature toggles:

- `[paths]` for external tools/scripts (`scripts`, `gothiczen`).
- `[features]` to enable/disable menu workflows (`batch_fix`, `container_check`, `chest_validation`, etc.).
- `[focus]` and `[chests.visual_map]` for rule lists and mappings.
- `[directories]`, `[validation]`, `[history]`, and `[logging]` for runtime behavior.

`chest_visual_map.json` has been folded into `[chests.visual_map]` in `config.toml`.

Example:

```toml
[paths]
scripts = "D:/Gothic Scripts/.../Content/Items"
gothiczen = "D:/Gothic Tools/GothicZEN/GothicZEN.exe"

[focus]
name_prefixes = ["MOBNAME_GRAVE", "MOBNAME_CHEST"]

[chests]
validate_visuals = true
auto_fix_wrong_locked_visuals = false

[chests.visual_map]
CHESTBIG_OCCHESTLARGELOCKED.MDS = "CHESTBIG_OCCHESTLARGE.MDS"

[directories]
input = "zenFix_Input"
output = "zenFix_Output"
instances = "zenFix_Instances"
broken = "zenFix_Broken"
logs = "zenFix_Log"
```

## Typical usage order (recommended)

1. **Scan Broken Instances (all ZENs)**
2. **Prompt Replacements (all lists)**
3. **Fix All Blocks (all ZENs)**
4. Optional: run **Check Containers** and **Check Chest Visuals**
5. Optional: run **Count zCVob Visual Usage** for visual audits

If you prefer one-click processing, use **Batch Fix**.
