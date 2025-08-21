# Photo Utils

A command-line toolkit for managing and processing photos, including duplicate removal, RAW conversion, EXIF export, organization, and aspect ratio checks.

## Features

- **Duplicate Cleaner:** Move duplicate files to a `_duplicates` folder.
- **ARW to JPG:** Batch convert Sony ARW RAW files to JPG.
- **ARW to DNG:** Batch convert ARW files to DNG using Adobe DNG Converter (macOS only).
- **EXIF to JSON:** Export EXIF metadata from all photos in a directory to a JSON file.
- **Organize by Date:** Move photos into folders by year and month-day based on EXIF date.
- **Aspect Ratio Tools:** Check or filter photos by aspect ratio.

## Setup (macOS)

1. **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd photo-utils
    ```

2. **Prepare the environment:**
    ```bash
    ./prepare_env.sh
    ```
    - This will create and activate a Python virtual environment.
    - It will check for required system dependencies (e.g., `exiftool`) and prompt to install them via Homebrew if missing.
    - Installs Python dependencies from `requirements.txt`.

3. **Activate the virtual environment (if not already active):**
    ```bash
    source venv/bin/activate
    ```

4. **Adobe DNG Converter (for ARW to DNG):**
    - Download and install [Adobe DNG Converter](https://helpx.adobe.com/photoshop/using/adobe-dng-converter.html) if you want to use the `arw2dng` command.
    - Default path: `/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter`

## Usage

Run the tool with:

```bash
python photo_utils.py <command> [options]
```

### Commands

#### 1. Clean Duplicates

Move duplicate files (by hash) to a `_duplicates` folder.

```bash
python photo_utils.py clean_dupes -src_dir <photos_dir> [--d]
```
- `--d`: Dry run, do not actually move files.

#### 2. Convert ARW to JPG

```bash
python photo_utils.py arw2jpg -src_dir <arw_dir> -dest_dir <jpg_dir>
```

#### 3. Convert ARW to DNG

```bash
python photo_utils.py arw2dng -src_dir <arw_dir> -dest_dir <dng_dir> [-converter_path <path_to_converter>]
```
- `-converter_path`: Optional, specify custom path to Adobe DNG Converter.

#### 4. Export EXIF to JSON

```bash
python photo_utils.py exif2json -src_dir <photos_dir> -dest_file <output.json>
```

#### 5. Organize Photos by Date

Moves photos into folders by year and month-day.

```bash
python photo_utils.py organize -src_dir <photos_dir> -dest_dir <organized_dir>
```

#### 6. Check Aspect Ratio

Prints photos matching (or not matching) a given aspect ratio.

```bash
python photo_utils.py check_aspect_ratio -src_dir <photos_dir> -aspect_ratio <W:H> [--all|--match|--not_match]
```
- `--all`: Print all photos (default)
- `--match`: Only matching
- `--not_match`: Only non-matching

#### 7. Get Photos by Aspect Ratio

Lists files with a specific aspect ratio.

```bash
python photo_utils.py get_by_aspect_ratio -src_dir <photos_dir> -aspect_ratio <W:H>
```

## Requirements

- macOS
- Python 3.8+
- [Homebrew](https://brew.sh/) (for system dependencies)
- exiftool (`brew install exiftool`)
- Adobe DNG Converter (for ARW to DNG conversion)

Python dependencies are listed in `requirements.txt` and installed by `prepare_env.sh`.

---

**Tip:** Always activate your virtual environment before running commands:
