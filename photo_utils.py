import argparse
import datetime
from pathlib import Path
import shutil
from helpers.get_metadata import get_exif_data
from helpers.simplify_ratio import simplify_ratio

def clean_dupes(args):
    print(f"Cleaning duplicates in directory: {args.src_dir}")
    # Here you would implement the logic to clean duplicate photos
    # For example, using file hashes or timestamps to identify duplicates

def convert_arw_to_jpg(args):
    print(f"Converting ARW files in directory: {args.src_dir} to JPG")
    # Here you would implement the logic to convert ARW files to JPG
    # This could involve using a library like PIL or OpenCV

def convert_arw_to_dng(args):
    print(f"Converting ARW files in directory: {args.src_dir} to DNG")
    # Here you would implement the logic to convert ARW files to JPG
    # This could involve using a library like PIL or OpenCV
    
def export_exif_to_json(args):
    from pathlib import Path
    import json
    src_dir = args.src_dir
    output_file = args.dest_file
    src_path = Path(src_dir)
    if not src_path.is_dir():
        raise ValueError(f"Directory not found: {src_dir}")

    print(f"Exporting EXIF data from directory: {src_dir} to JSON file: {output_file}")

    result = get_exif_data(src_path)
    
    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))

    print(f"EXIF metadata written to: {output_file}")
    
def organize_photos(args):
    src_dir = Path(args.src_dir)
    dest_dir = Path(args.dest_dir)

    if not src_dir.exists() or not src_dir.is_dir():
        print(f"Source directory does not exist: {src_dir}")
        return

    print(f"Organizing photos from directory: {src_dir} to {dest_dir}")

    try:
        exif_data = get_exif_data(src_dir, type="all")
    except RuntimeError as e:
        print(e)
        return

    for entry in exif_data:
        try:
            src_file = Path(entry["SourceFile"])
            date_str = entry.get("DateTimeOriginal") or entry.get("CreateDate") or entry.get("ModifyDate")
            if not date_str:
                print(f"No date found for {src_file}, skipping.")
                continue

            # exiftool format: "2023:07:28 14:05:01"
            date_taken = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            year = date_taken.strftime("%Y")
            month_day = date_taken.strftime("%m-%d")

            target_dir = dest_dir / year / month_day
            target_dir.mkdir(parents=True, exist_ok=True)

            dest_file = target_dir / src_file.name
            if dest_file.exists():
                print(f"File already exists: {dest_file}, skipping.")
                continue

            shutil.move(str(src_file), str(dest_file))
            print(f"Moved: {src_file} -> {dest_file}")

        except Exception as e:
            print(f"Failed to process {entry.get('SourceFile', 'unknown')}: {e}")
    

def check_aspect_ratio(args):
    print(f"Checking aspect ratio in directory: {args.src_dir} for aspect ratio: {args.aspect_ratio}")
    # Determine mode, default to 'all' if none specified
    if not (args.all or args.match or args.not_match):
        args.all = True
    target_w, target_h = map(int, args.aspect_ratio.split(':'))
    target_w, target_h = simplify_ratio(target_w, target_h)

    photos_data = get_exif_data(args.src_dir)
    for photo in photos_data:
        if 'ImageWidth' in photo and 'ImageHeight' in photo:
            width = photo['ImageWidth']
            height = photo['ImageHeight']
            w, h = simplify_ratio(width, height)
            if (w, h) == (target_w, target_h) and (args.all or args.match):
                print(f"Photo {photo['SourceFile']} matches aspect ratio {args.aspect_ratio}")
            elif (w, h) != (target_w, target_h) and (args.all or args.not_match):
                print(f"Photo {photo['SourceFile']} does not match aspect ratio {args.aspect_ratio} (actual: {w}:{h})")
        else:
            print(f"Photo {photo['SourceFile']} does not have width/height data")

def get_by_aspect_ratio(src_dir, aspect_ratio):
    print(f"Getting photos by aspect ratio {aspect_ratio} in directory: {src_dir}")
    # Here you would implement the logic to filter photos by aspect ratio
    # This could involve reading image dimensions and comparing them to the specified aspect ratio
    
def main():
    parser = argparse.ArgumentParser(description="Photography utilities command line tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Sub-command: clean_dupes    
    parser_something = subparsers.add_parser('clean_dupes', help='Clean duplicate photos')
    parser_something.add_argument('-src_dir', required=True, help='Source directory containing photos')
    parser_something.set_defaults(func=clean_dupes)

    # Sub-command: arw2jpg
    parser_something_else = subparsers.add_parser('arw2jpg', help='Convert ARW files to JPG')
    parser_something_else.add_argument('-src_dir', required=True, help='Source directory containing ARW files')
    parser_something_else.add_argument('-dest_dir', required=True, help='Destination directory for converted JPG files')
    parser_something_else.set_defaults(func=convert_arw_to_jpg)
    
    # Sub-command: arw2dng
    parser_something_else = subparsers.add_parser('arw2dng', help='Convert ARW files to DNG')
    parser_something_else.add_argument('-src_dir', required=True, help='Source directory containing ARW files')
    parser_something_else.add_argument('-dest_dir', required=True, help='Destination directory for converted JPG files')
    parser_something_else.set_defaults(func=convert_arw_to_dng)
    
    # Sub-command: exif2json
    parser_something_else = subparsers.add_parser('exif2json', help='Convert EXIF data to JSON')
    parser_something_else.add_argument('-src_dir', required=True, help='Source directory containing photos')
    parser_something_else.add_argument('-dest_file', required=True, help='Destination JSON file for EXIF data')
    parser_something_else.set_defaults(func=export_exif_to_json)
    
    # Sub-command: organize
    parser_something_else = subparsers.add_parser('organize', help='Organize photos by date')
    parser_something_else.add_argument('-src_dir', required=True, help='Source directory containing photos')
    parser_something_else.add_argument('-dest_dir', required=True, help='Destination directory for organized photos')
    parser_something_else.set_defaults(func=organize_photos)
    
    # Sub-command: check_aspect_ratio
    parser_something_else = subparsers.add_parser('check_aspect_ratio', help='Check aspect ratio of photos')
    parser_something_else.add_argument('-src_dir', required=True, help='Source directory containing photos')
    parser_something_else.add_argument('-aspect_ratio', required=True, help='Aspect ratio to check (e.g., 16:9)')
    group = parser_something_else.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true', help='Print all photos')
    group.add_argument('--match', action='store_true', help='Print only matching photos')
    group.add_argument('--not_match', action='store_true', help='Print only non-matching photos')
    parser_something_else.set_defaults(func=check_aspect_ratio)
  
    # Sub-command: get_by_aspect_ratio
    parser_something_else = subparsers.add_parser('get_by_aspect_ratio', help='Get photos by aspect ratio')
    parser_something_else.add_argument('-src_dir', required=True, help='Source directory containing photos')
    parser_something_else.add_argument('-aspect_ratio', required=True, help='Aspect ratio to filter by (e.g., 16:9)')
    parser_something_else.set_defaults(func=get_by_aspect_ratio)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()