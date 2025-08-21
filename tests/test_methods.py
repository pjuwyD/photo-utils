import os
import sys
import shutil
import tempfile
import pytest
from pathlib import Path

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from photo_utils import (
    clean_dupes,
    convert_arw_to_jpg,
    convert_arw_to_dng,
    export_exif_to_json,
    organize_photos,
)

class Args:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def test_dir(tmp_path):
    # Copy src_files to a temp directory for isolation
    src = Path(__file__).parent / "src_files"
    dst = tmp_path / "src_files"
    shutil.copytree(src, dst)
    return dst

def test_clean_dupes(test_dir):
    # Duplicate the jpg file
    jpg_file = next(test_dir.glob("*.JPG"))
    dup_file = test_dir / f"copy_{jpg_file.name}"
    shutil.copy(jpg_file, dup_file)
    args = Args(src_dir=str(test_dir), d=False)
    clean_dupes(args)
    assert (test_dir / "_duplicates").exists()
    assert not dup_file.exists() or not jpg_file.exists()
    

def test_convert_arw_to_jpg(test_dir, tmp_path):
    out_dir = tmp_path / "jpg"
    out_dir.mkdir()
    args = Args(src_dir=str(test_dir), dest_dir=str(out_dir))
    convert_arw_to_jpg(args)
    jpgs = list(out_dir.glob("*.jpg"))
    assert len(jpgs) > 0

@pytest.mark.skipif(
    not Path("/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter").exists(),
    reason="Adobe DNG Converter not installed"
)
def test_convert_arw_to_dng(test_dir, tmp_path):
    out_dir = tmp_path / "dng"
    out_dir.mkdir()
    args = Args(src_dir=str(test_dir), dest_dir=str(out_dir), converter_path=None)
    convert_arw_to_dng(args)
    dngs = list(out_dir.glob("*.dng"))
    assert len(dngs) > 0

def test_export_exif_to_json(test_dir, tmp_path):
    out_file = tmp_path / "exif.json"
    args = Args(src_dir=str(test_dir), dest_file=str(out_file))
    export_exif_to_json(args)
    assert out_file.exists()
    with open(out_file) as f:
        data = f.read()
        assert "SourceFile" in data

def test_organize_photos(test_dir, tmp_path):
    out_dir = tmp_path / "organized"
    args = Args(src_dir=str(test_dir), dest_dir=str(out_dir))
    organize_photos(args)
    year_dirs = list(out_dir.iterdir())
    assert any(d.is_dir() and d.name == "2025" for d in year_dirs)
    month_day_dirs = list((out_dir / "2025").iterdir())
    assert any(d.is_dir() and d.name == "05-02" for d in month_day_dirs)
    # Should move at least one file into the correct folder
    files = list((out_dir / "2025" / "05-02").iterdir())
    assert len(files) > 0