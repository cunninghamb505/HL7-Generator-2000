"""Build script for HL7 Generator 2000 Windows installer.

Usage:
    python build_installer.py          Build PyInstaller bundle + Inno Setup installer
    python build_installer.py --skip-installer   Only build the PyInstaller bundle
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC_FILE = ROOT / "hl7gen.spec"
ISS_FILE = ROOT / "installer.iss"
DIST_DIR = ROOT / "dist" / "hl7gen"
INSTALLER_DIR = ROOT / "installer"
ISCC_PATH = Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe")


def run(cmd: list[str], label: str) -> None:
    """Run a subprocess, streaming output and raising on failure."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, cwd=str(ROOT))
    if result.returncode != 0:
        print(f"\nERROR: {label} failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def build_pyinstaller() -> None:
    """Run PyInstaller to produce the dist/hl7gen/ bundle."""
    if DIST_DIR.exists():
        print(f"Cleaning previous build: {DIST_DIR}")
        shutil.rmtree(DIST_DIR)

    run(
        [sys.executable, "-m", "PyInstaller", "--noconfirm", str(SPEC_FILE)],
        "PyInstaller Build",
    )

    if not DIST_DIR.exists():
        print(f"ERROR: Expected output not found at {DIST_DIR}")
        sys.exit(1)

    # Count files for a quick sanity check
    file_count = sum(1 for _ in DIST_DIR.rglob("*") if _.is_file())
    print(f"\nPyInstaller bundle: {DIST_DIR}")
    print(f"  Files: {file_count}")


def build_inno_setup() -> None:
    """Run Inno Setup compiler to produce the .exe installer."""
    if not ISCC_PATH.exists():
        print(f"ERROR: Inno Setup compiler not found at {ISCC_PATH}")
        print("Install Inno Setup 6 from https://jrsoftware.org/isinfo.php")
        sys.exit(1)

    INSTALLER_DIR.mkdir(exist_ok=True)

    run(
        [str(ISCC_PATH), str(ISS_FILE)],
        "Inno Setup Compiler",
    )

    installer_exe = INSTALLER_DIR / "HL7Generator2000-Setup.exe"
    if installer_exe.exists():
        size_mb = installer_exe.stat().st_size / (1024 * 1024)
        print(f"\nInstaller created: {installer_exe}")
        print(f"  Size: {size_mb:.1f} MB")
    else:
        print(f"ERROR: Expected installer not found at {installer_exe}")
        sys.exit(1)


def main() -> None:
    skip_installer = "--skip-installer" in sys.argv

    print("HL7 Generator 2000 - Build Script")
    print(f"  Python:       {sys.version}")
    print(f"  Project root: {ROOT}")
    print(f"  Spec file:    {SPEC_FILE}")
    if not skip_installer:
        print(f"  ISS file:     {ISS_FILE}")
        print(f"  ISCC path:    {ISCC_PATH}")

    # Step 1: PyInstaller
    build_pyinstaller()

    # Step 2: Inno Setup
    if skip_installer:
        print("\nSkipping Inno Setup (--skip-installer flag)")
    else:
        build_inno_setup()

    print(f"\n{'='*60}")
    print("  BUILD COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
