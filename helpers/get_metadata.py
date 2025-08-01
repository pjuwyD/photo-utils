import subprocess
import shutil
import json

def get_exif_data(directory, type=None):
    # Ensure exiftool is installed
    if not shutil.which("exiftool"):
        raise RuntimeError("exiftool not found. Install it first (brew install exiftool or apt install libimage-exiftool-perl)")
    # Run exiftool on all .ARW files and get output as JSON
    command = ["exiftool", "-r", "-json", "-ext", "ARW", str(directory)]
    if type == "all":
        command = ["exiftool", "-r", "-json", str(directory)]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        )
    if result.returncode != 0:
        print(f"Exiftool error:\n{result.stderr}")
        raise RuntimeError("Exiftool failed")

    return json.loads(result.stdout) if result.stdout else []
