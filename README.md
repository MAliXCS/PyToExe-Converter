<div align="center">

```
██████╗ ██╗   ██╗    ██████╗     ███████╗██╗  ██╗███████╗
██╔══██╗╚██╗ ██╔╝    ╚════██╗    ██╔════╝╚██╗██╔╝██╔════╝
██████╔╝ ╚████╔╝      █████╔╝    █████╗   ╚███╔╝ █████╗
██╔═══╝   ╚██╔╝       ╚═══██╗    ██╔══╝   ██╔██╗ ██╔══╝
██║        ██║        ██████╔╝   ███████╗██╔╝ ██╗███████╗
╚═╝        ╚═╝        ╚═════╝    ╚══════╝╚═╝  ╚═╝╚══════╝
```

# PyToExe Converter — v2.1

### Convert any Python script into a standalone Windows `.exe` — no terminal, no hassle.

[![Python](https://img.shields.io/badge/Python-3.6%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Windows-7%20%7C%208%20%7C%2010%20%7C%2011-0078d4?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-238636?style=for-the-badge)](LICENSE)
[![Backend](https://img.shields.io/badge/Engine-PyInstaller-e74c3c?style=for-the-badge)](https://pyinstaller.org)
[![GUI](https://img.shields.io/badge/GUI-tkinter%20%28built--in%29-f39c12?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)

---

**Author** &nbsp;→&nbsp; Instagram [@x404ctl](https://instagram.com/x404ctl) &nbsp;|&nbsp; GitHub [@MAliXCS](https://github.com/MAliXCS)

</div>

---

## What is PyToExe?

**PyToExe Converter** is a professional, dark-themed desktop GUI application that wraps PyInstaller into a clean, one-click interface. You select your `.py` file, pick your options, press **CONVERT** — and get a fully standalone `.exe` that runs on any Windows machine, even without Python installed.

No terminal knowledge required. No command memorisation. No configuration files. Just point, click, and convert.

---

## Preview

```
┌─────────────────────────────────────────────────────────────────────┐
│  [ PY ]  PyToExe  Converter        Instagram @x404ctl | GitHub @MAliX │
├─────────────────────────────────────────────────────────────────────┤
│  01 / Select Files                                                   │
│    Python Script * │ C:\projects\myapp.py              │ [ Browse ] │
│    Output Folder   │ C:\projects\dist                  │ [ Browse ] │
│    Icon  (.ico)    │ C:\assets\myicon.ico              │ [ Browse ] │
├─────────────────────────────────────────────────────────────────────┤
│  02 / Build Options                                                  │
│    [x] One-File (single .exe)    [ ] Windowed (no console)          │
├─────────────────────────────────────────────────────────────────────┤
│  03 / Additional Files (optional)                                    │
│    │ config.json                          │  [ + Add ]              │
│    │ data.db                              │  [ - Remove ]           │
├─────────────────────────────────────────────────────────────────────┤
│  04 / Python Interpreter (detected automatically)                    │
│    C:\Python311\python.exe                         [ Change ]       │
├─────────────────────────────────────────────────────────────────────┤
│  ╔═════════════════════════════════════════════════════════════════╗ │
│  ║           CONVERT   .py  -->  .exe                             ║ │
│  ╚═════════════════════════════════════════════════════════════════╝ │
│  [████████████████████░░░░] Building...              [ Clear Log ] │
│  [ Open Output Folder ]                                              │
├─────────────────────────────────────────────────────────────────────┤
│  05 / Build Log                                                      │
│  [ 14:32:01 ]  Build started                                        │
│  Python     : C:\Python311\python.exe                               │
│  Script     : C:\projects\myapp.py                                  │
│  INFO: Analyzing myapp.py ...                                       │
│  INFO: Building EXE ...                                             │
│  [ 14:32:18 ]  Build succeeded                                      │
│  Executable : C:\projects\dist\myapp.exe                            │
├─────────────────────────────────────────────────────────────────────┤
│  ● Done.  myapp.exe  -->  C:\projects\dist                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Features

| Feature | Description |
|---|---|
| **Splash Screen** | Terminal-style boot animation with typewriter effect on every launch |
| **Auto Python Detection** | Finds `python.exe` automatically, even when app is itself packaged as `.exe` |
| **One-File Mode** | Entire app packed into a single portable `.exe` |
| **One-Folder Mode** | Outputs a folder with `.exe` + dependencies (faster startup) |
| **Console / Windowed** | Toggle terminal window on or off for the output exe |
| **Custom Icon** | Embed any `.ico` file directly into the executable |
| **Bundle Extra Files** | Include data files, configs, assets, databases |
| **Live Build Log** | Real-time colour-coded PyInstaller output streamed to screen |
| **Auto-Install PyInstaller** | Detects missing PyInstaller and installs it silently |
| **EXE Verification** | Confirms the `.exe` actually exists after build (catches antivirus deletions) |
| **Open Output Folder** | One-click to open the output directory in Windows Explorer |
| **Dark Professional Theme** | GitHub-style dark UI throughout — no white flash, no ugly defaults |
| **Zero Extra Dependencies** | Only `tkinter` (built-in) + `PyInstaller` |

---

## What You Need to Install

> See [INSTALL.md](INSTALL.md) for the full step-by-step installation guide.

### Minimum Requirements

| Requirement | Version | Notes |
|---|---|---|
| **Python** | 3.6 or newer | Must be installed and on PATH |
| **tkinter** | Built into Python | No extra install needed on Windows |
| **PyInstaller** | Any recent version | Auto-installed by the app if missing |
| **Windows OS** | 7 / 8 / 10 / 11 | Primary supported platform |
| **RAM** | 256 MB free | More needed for large builds |
| **Disk Space** | ~500 MB free | For PyInstaller build cache |

### Quick Install

```bash
# Step 1 — Install Python (if not already installed)
# Download from: https://python.org/downloads
# IMPORTANT: Check "Add Python to PATH" during installation

# Step 2 — Install PyInstaller
pip install pyinstaller

# Step 3 — Run PyToExe
python py2exe_converter.py
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/MAliXCS/pytoexe-converter.git
cd pytoexe-converter

# Run
python py2exe_converter.py
```

The splash screen will appear. Press any key — then you're in.

---

## Repository Structure

```
pytoexe-converter/
│
├── py2exe_converter.py     ← The entire application (single file)
├── README.md               ← This file
├── INSTALL.md              ← Full installation guide for all setups
├── HOW_TO_USE.md           ← Complete step-by-step usage guide
├── ABOUT.md                ← App background, specs, architecture, design
├── CHANGELOG.md            ← Version history and changes
├── LICENSE                 ← MIT License
└── .gitignore              ← Ignores build artifacts
```

---

## How It Works (Simple)

```
  Your .py script
       │
       ▼
  PyToExe GUI  ──►  Builds PyInstaller command  ──►  Runs it in background
       │                                                      │
       ▼                                                      ▼
  Live log streams to screen                     .exe saved to output folder
```

Internally, the app calls:
```bash
python -m PyInstaller --onefile --console --icon app.ico --distpath C:\dist yourscript.py
```
…but you never have to type or remember any of that.

---

## Known Limitations

- **Windows only for `.exe` output.** PyInstaller does not cross-compile — macOS produces `.app`, Linux produces ELF binaries.
- **Antivirus false positives.** Fresh PyInstaller executables are commonly (and wrongly) flagged. The app detects this and tells you how to fix it.
- **Python 2 not supported.**
- **Large apps take longer.** Scripts with many dependencies (numpy, pandas, tensorflow) can take 2–5 minutes to build.

---

## Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m "Add your idea"`
4. Push: `git push origin feature/your-idea`
5. Open a Pull Request

Bug reports and feature requests are welcome via [GitHub Issues](https://github.com/MAliX/pytoexe-converter/issues).

---

## License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

<div align="center">

Made with Python &nbsp;·&nbsp; Powered by PyInstaller &nbsp;·&nbsp; by [@x404ctl](https://instagram.com/x404ctl) & [@MAliXCS](https://github.com/MAliXCS)

</div>
