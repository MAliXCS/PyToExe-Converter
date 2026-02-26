# Changelog

All notable changes to PyToExe Converter are documented here.

---

## [v2.1] — Bug Fix Release

### Fixed
- **CRITICAL:** `sys.executable` now resolves to real `python.exe` even when PyToExe is itself packaged as a `.exe` (frozen exe detection via `sys.frozen`)
- **CRITICAL:** `build_command()` return value corrected — was returning tuple inconsistently, causing silent thread crash
- Thread no longer permanently disables CONVERT button if any exception occurs — `_unlock_ui()` is now always called on exit
- Removed `--clean` flag which caused file-lock errors on Windows with certain antivirus tools
- Removed `cwd=` subprocess override which caused drive-letter path conflicts on multi-drive systems
- Fixed exe not found after successful build — now verified with `os.path.isfile()` after PyInstaller exits

### Added
- **Section 04 — Python Interpreter panel** showing exactly which `python.exe` will be used
- **Change button** in Section 04 to manually select a different `python.exe` (virtual environments, multiple installs)
- **Three distinct build outcomes:** real success + exe found / build OK but exe missing (antivirus) / real failure
- Specific antivirus detection with fix instructions in both log and popup
- Early warning at startup if no Python interpreter can be found
- Detailed path info logged at build start (Python path, script path, output path)

### Changed
- Version bump from v2.0 to v2.1
- Splash screen updated to show v2.1 and new boot message about locating Python

---

## [v2.0] — Major Rewrite

### Added
- Complete dark GitHub-style theme throughout (replaces light grey default)
- Terminal-style splash screen with typewriter animation on launch
- "Press any key to continue..." with blinking cursor
- Scrollable main canvas (mouse wheel support)
- Timestamped build log entries `[ HH:MM:SS ]`
- Colour-coded log output (green/red/orange/cyan/yellow)
- "Open Output Folder" button appearing after successful build
- Status bar with coloured dot indicator (grey/blue/green/orange/red)
- Title bar with `[ PY ]` badge and author info
- Card-style numbered sections (01–05)
- Progress bar showing build activity

### Changed
- Section numbering added (01–05) for clarity
- Build log moved to scrolledtext widget with full colour tagging
- All paths converted to absolute before passing to PyInstaller
- Window title includes author handles

---

## [v1.0] — Initial Release

### Added
- Basic tkinter GUI for PyInstaller
- Python script file selection
- Output folder selection
- Icon (.ico) selection
- One-File / One-Folder toggle
- Console / Windowed toggle
- Additional files list with Add/Remove
- Build log (plain text)
- Auto-install of PyInstaller if missing
- Basic success/failure messagebox

---

<div align="center">

Instagram [@x404ctl](https://instagram.com/x404ctl) &nbsp;|&nbsp; GitHub [@MAliXCS](https://github.com/MAliXCS)

</div>
