# Installation Guide

> Everything you need to install before running PyToExe Converter.
>
> **Author:** Instagram [@x404ctl](https://instagram.com/x404ctl) &nbsp;|&nbsp; GitHub [@MAliXCS](https://github.com/MAliXCS)

---

## Table of Contents

1. [What You Need](#1-what-you-need)
2. [Install Python](#2-install-python)
3. [Verify Python Works](#3-verify-python-works)
4. [Install PyInstaller](#4-install-pyinstaller)
5. [Download PyToExe](#5-download-pytoexe)
6. [Run PyToExe](#6-run-pytoexe)
7. [Troubleshooting Install Problems](#7-troubleshooting-install-problems)
8. [Uninstalling Everything](#8-uninstalling-everything)

---

## 1. What You Need

Before you can run PyToExe Converter, you need exactly **two things** installed on your Windows machine:

| What | Why | Where to Get It |
|---|---|---|
| **Python 3.6+** | PyToExe is written in Python and needs Python to run | [python.org/downloads](https://python.org/downloads) |
| **PyInstaller** | The engine that does the actual `.py` → `.exe` conversion | Auto-installed by PyToExe, or: `pip install pyinstaller` |

That is it. Nothing else. No Visual Studio, no compilers, no .NET, no admin rights required for normal use.

---

## 2. Install Python

### Step 1 — Download Python

Go to **[https://python.org/downloads](https://python.org/downloads)**

Click the big yellow **"Download Python 3.x.x"** button (the latest stable version).

> Recommended: Python 3.10, 3.11, or 3.12 for best PyInstaller compatibility.

### Step 2 — Run the Installer

Double-click the downloaded `.exe` file.

**CRITICAL — Before clicking Install Now:**

```
┌──────────────────────────────────────────────────┐
│  Install Python 3.xx                             │
│                                                  │
│  [x] Install launcher for all users             │
│  [x] Add Python 3.xx to PATH    ← CHECK THIS!   │
│                                                  │
│  [ Install Now ]  [ Customize installation ]     │
└──────────────────────────────────────────────────┘
```

**You MUST check "Add Python to PATH"** — if you miss this, nothing will work and you will have to reinstall.

Then click **Install Now** and wait for it to finish (usually 1–2 minutes).

### Step 3 — Click "Close"

When you see "Setup was successful", click Close.

---

## 3. Verify Python Works

Open **Command Prompt**:
- Press `Win + R`
- Type `cmd`
- Press Enter

Then type:

```
python --version
```

You should see something like:

```
Python 3.11.4
```

If you see that — Python is installed correctly. Move to Step 4.

**If you see an error** like `'python' is not recognized`:

```
# Try this instead:
py --version

# Or this:
python3 --version
```

If none of those work, Python was not added to PATH. You need to either:
- Reinstall Python and check the "Add to PATH" box this time, OR
- Add it manually: see [Troubleshooting](#7-troubleshooting-install-problems)

---

## 4. Install PyInstaller

> **You can skip this step.** PyToExe will detect that PyInstaller is missing and offer to install it automatically when you first press CONVERT.

But if you prefer to install it manually, open Command Prompt and run:

```bash
pip install pyinstaller
```

Wait for it to download and install (requires internet, usually takes 30–60 seconds).

Verify it installed:

```bash
pyinstaller --version
```

You should see a version number like `6.3.0`.

---

## 5. Download PyToExe

### Option A — Download ZIP (easiest)

1. Go to: **[github.com/MAliXCS/pytoexe-converter](https://github.com/MAliXCS/pytoexe-converter)**
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP anywhere you want, e.g. `C:\Tools\PyToExe\`

### Option B — Clone with Git

If you have Git installed:

```bash
git clone https://github.com/MAliXCS/pytoexe-converter.git
```

### Option C — Single File

The entire application is just one file: **`py2exe_converter.py`**

You can download just that one file and put it anywhere on your computer.

---

## 6. Run PyToExe

### Method 1 — Double-click (easiest)

Right-click `py2exe_converter.py` → **Open with** → **Python**

If you don't see Python in the list:
- Click "Choose another app"
- Browse to `C:\Python311\python.exe` (or wherever Python installed)
- Check "Always use this app"
- Click OK

### Method 2 — Command Prompt (most reliable)

```bash
cd C:\Tools\PyToExe
python py2exe_converter.py
```

### Method 3 — Create a Desktop Shortcut

1. Right-click on your Desktop → **New** → **Shortcut**
2. In the location field, type:
   ```
   python C:\Tools\PyToExe\py2exe_converter.py
   ```
   (use your actual path)
3. Click **Next**, name it `PyToExe`, click **Finish**
4. Double-click the shortcut anytime to launch

### First Launch

The **splash screen** will appear with a typing animation. Press any key or click anywhere to enter the main application.

If PyInstaller is not installed, you will be asked to install it. Click **Yes** — it will install automatically.

---

## 7. Troubleshooting Install Problems

### "python is not recognized as an internal or external command"

Python is not on your system PATH.

**Fix Option A — Reinstall Python:**
- Download Python again from python.org
- Run the installer
- This time, on the first screen, **CHECK "Add Python to PATH"**
- Finish installation
- Open a NEW Command Prompt and try again

**Fix Option B — Add to PATH manually:**
1. Press `Win + S`, search for "Environment Variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables..."
4. Under "System variables", find and click "Path", click "Edit"
5. Click "New"
6. Add: `C:\Python311` (or wherever Python is installed)
7. Click "New" again
8. Add: `C:\Python311\Scripts`
9. Click OK on all windows
10. Open a **new** Command Prompt and try `python --version` again

---

### "pip is not recognized"

pip is Python's package installer and should come with Python.

```bash
# Try this instead
python -m pip install pyinstaller

# Or
py -m pip install pyinstaller
```

If pip is missing entirely:

```bash
python -m ensurepip --upgrade
```

---

### "pip install pyinstaller" fails with permission error

```bash
# Add --user flag to install for current user only
pip install pyinstaller --user
```

---

### PyInstaller installs but PyToExe still says it's missing

This usually happens when you have multiple Python versions installed. PyToExe found a different Python than where you installed PyInstaller.

**Fix:** Use the **"Change"** button in Section 04 of the app to manually point to the correct `python.exe` where PyInstaller is installed.

---

### The app opens but immediately closes

You probably double-clicked `py2exe_converter.py` without Python set as the default program.

**Fix:** Open Command Prompt and run:
```bash
python C:\path\to\py2exe_converter.py
```
You will see any error messages in the terminal.

---

### "No module named tkinter"

This is rare on Windows but can happen with minimal Python installs.

**Fix:** Reinstall Python from python.org using the standard installer (not the Microsoft Store version). The standard installer always includes tkinter.

---

### Windows Defender or Antivirus blocks the output .exe

This is a **false positive** — a known, documented issue with all PyInstaller-built executables. The app is safe.

**Fix:**
1. Open Windows Security → Virus & threat protection
2. Click "Manage settings" under "Virus & threat protection settings"
3. Scroll to "Exclusions" → "Add or remove exclusions"
4. Add your output folder (e.g. `C:\projects\dist`)
5. Build again

---

## 8. Uninstalling Everything

### Remove PyToExe

Just delete the `py2exe_converter.py` file (and its folder if you made one).
No registry entries. No system changes. Nothing else to remove.

### Remove PyInstaller

```bash
pip uninstall pyinstaller
```

### Remove Python

Go to **Settings → Apps → Installed Apps**, find Python, click Uninstall.

### Clean up build artifacts

Delete any folders named:
- `dist/`
- `__pybuild_tmp__/`
- Any `.spec` files

These are all in the same folder as whatever scripts you converted.

---

<div align="center">

Instagram [@x404ctl](https://instagram.com/x404ctl) &nbsp;|&nbsp; GitHub [@MAliXCS](https://github.com/MAliXCS)

</div>
