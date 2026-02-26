# How to Use PyToExe Converter

> A complete, step-by-step guide covering every feature of the app.
>
> **Author:** Instagram [@x404ctl](https://instagram.com/x404ctl) &nbsp;|&nbsp; GitHub [@MAliXCS](https://github.com/MAliXCS)

---

## Table of Contents

1. [Launching the App](#1-launching-the-app)
2. [The Splash Screen](#2-the-splash-screen)
3. [Understanding the Interface](#3-understanding-the-interface)
4. [Section 01 — Select Files](#4-section-01--select-files)
5. [Section 02 — Build Options](#5-section-02--build-options)
6. [Section 03 — Additional Files](#6-section-03--additional-files)
7. [Section 04 — Python Interpreter](#7-section-04--python-interpreter)
8. [The CONVERT Button](#8-the-convert-button)
9. [The Build Log](#9-the-build-log)
10. [After a Successful Build](#10-after-a-successful-build)
11. [Basic Conversion — Step by Step](#11-basic-conversion--step-by-step)
12. [Advanced Conversion — Step by Step](#12-advanced-conversion--step-by-step)
13. [Common Errors and How to Fix Them](#13-common-errors-and-how-to-fix-them)
14. [Pro Tips](#14-pro-tips)

---

## 1. Launching the App

Open **Command Prompt** (`Win + R` → type `cmd` → Enter) and run:

```bash
python py2exe_converter.py
```

Or right-click the file in Explorer → **Open with Python**.

---

## 2. The Splash Screen

Every time you open PyToExe, a terminal-style splash screen appears:

```
  ██████╗ ██╗   ██╗    ██████╗     ███████╗██╗  ██╗███████╗
  ...

  Python  -->  EXE  Converter   v2.1
  Author  :  Instagram @x404ctl   |   GitHub @MAliXCS

  ──────────────────────────────────────────────────────────

  [ * ]  Initializing runtime environment ...
  [ * ]  Locating Python interpreter ...
  [ * ]  Loading PyInstaller interface ...
  [ * ]  Configuring build workspace ...
  [ * ]  All systems ready.

  ──────────────────────────────────────────────────────────

        Press any key to continue ..._
```

**How to dismiss it:**
- Press **any key** on your keyboard, OR
- **Click anywhere** on the splash window

The main app opens immediately after.

---

## 3. Understanding the Interface

The app is divided into **5 numbered sections** plus a CONVERT button, progress bar, and status bar:

```
┌─────────────────────────────────────────────────────┐
│  TITLE BAR  ( app name + author )                   │
├─────────────────────────────────────────────────────┤
│  01 / Select Files          ← your .py, output, icon│
│  02 / Build Options         ← one-file, windowed    │
│  03 / Additional Files      ← bundle extra data     │
│  04 / Python Interpreter    ← shows python.exe path │
├─────────────────────────────────────────────────────┤
│  [ CONVERT  .py  -->  .exe ]  ← THE BIG BUTTON      │
│  [progress bar]   [Clear Log]                        │
│  [ Open Output Folder ]    ← appears after success  │
├─────────────────────────────────────────────────────┤
│  05 / Build Log             ← live build output     │
├─────────────────────────────────────────────────────┤
│  STATUS BAR  ( coloured dot + message )             │
└─────────────────────────────────────────────────────┘
```

| Status Dot Colour | Meaning |
|---|---|
| Grey | Ready / idle |
| Blue | Build in progress |
| Green | Build succeeded |
| Orange | Build finished but something is off (antivirus?) |
| Red | Build failed |

---

## 4. Section 01 — Select Files

This section has three fields:

### Python Script (required)

Click **Browse** → navigate to your `.py` or `.pyw` file → click Open.

The path fills in automatically. The Output Folder also auto-fills to a `dist/` folder next to your script (you can change it).

> Your script must be runnable as-is before converting. Always test it with `python yourscript.py` first.

### Output Folder (optional)

Where your `.exe` will be saved. Defaults to `dist/` next to your script.

Click **Browse** to pick a different folder.

### Icon (.ico) (optional)

Click **Browse** → select a `.ico` file to embed as the executable's icon.

The icon appears in Windows Explorer, on the taskbar, and in the title bar when the exe runs.

> **Need to convert a PNG to ICO?**
> Use [convertico.com](https://convertico.com) or install Pillow:
> ```bash
> pip install pillow
> python -c "from PIL import Image; Image.open('icon.png').save('icon.ico')"
> ```

---

## 5. Section 02 — Build Options

Two checkboxes control how the output is built:

### One-File (checked by default)

| State | What Happens |
|---|---|
| **Checked** | Everything is packed into a **single `.exe`** file. Easy to share. Slightly slower to launch because it extracts itself each run. |
| **Unchecked** | Output is a **folder** containing the `.exe` plus all dependencies side-by-side. Faster to launch. Easier to update individual files. |

**Recommendation:** Use One-File for simple tools you want to share. Use One-Folder for large apps or when startup speed matters.

### Windowed (unchecked by default)

| State | What Happens |
|---|---|
| **Unchecked** | A black **console/terminal window** appears when the exe runs. Good for scripts, CLI tools, and debugging. |
| **Checked** | **No terminal window** — the exe launches silently. Required for GUI apps (tkinter, PyQt, etc.) that should look like normal Windows apps. |

> **Warning:** If you use Windowed mode and your script has a bug, you will see nothing when it crashes — no error message, nothing. Always confirm your script works correctly in Console mode first, then switch to Windowed.

---

## 6. Section 03 — Additional Files

If your Python script reads external files at runtime — config files, databases, images, text files, CSV data — those files must be **bundled into the build**. Otherwise the exe will crash with a `FileNotFoundError`.

### Adding Files

Click **+ Add** → select one or more files → they appear in the list.

### Removing Files

Click a file in the list to select it → click **- Remove**.

### Accessing Bundled Files in Your Code

When running as a normal `.py`, files are next to your script. When running as a frozen `.exe`, bundled files are extracted to a temporary folder. You need to handle both cases in your code:

```python
import sys
import os

def resource_path(relative_name):
    """Get the absolute path to a bundled resource file."""
    if getattr(sys, 'frozen', False):
        # Running as .exe — files are in sys._MEIPASS
        base = sys._MEIPASS
    else:
        # Running as .py — files are next to the script
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_name)

# Usage:
config_path = resource_path("config.json")
image_path  = resource_path("logo.png")
db_path     = resource_path("data.db")
```

Add this function to any script that reads external files before converting it.

---

## 7. Section 04 — Python Interpreter

This section shows which `python.exe` PyToExe has detected on your system.

```
  C:\Python311\python.exe                          [ Change ]
```

- **Green text** = Python found and verified ✓
- **Red text** = Python not found — you must fix this before building

### Why This Matters

When PyToExe is run as a plain `.py` file, Python is obvious. But if someone has packaged PyToExe itself into an `.exe`, the app can no longer assume `sys.executable` is Python — it might point to itself. Section 04 shows you exactly which Python will be used so there are no surprises.

### Changing the Python Interpreter

Click **Change** to manually browse to a `python.exe`. This is useful when:
- You have multiple Python versions installed and want to use a specific one
- You are using a virtual environment's Python
- Auto-detection found the wrong Python

---

## 8. The CONVERT Button

The big green button in the middle of the app. Press it to start the build.

**States:**

| Button State | Meaning |
|---|---|
| Green — "CONVERT .py --> .exe" | Ready to build |
| Grey — "Building ... please wait" | Build in progress, disabled |
| Returns to green | Build finished (success or failure) |

After a successful build, a green **"Open Output Folder"** button appears below the CONVERT button. Click it to jump straight to your `.exe` in Windows Explorer.

---

## 9. The Build Log

Section 05 shows live output from PyInstaller while your script is being compiled.

### Colour Guide

| Colour | What It Means |
|---|---|
| **Yellow** | Timestamp headers — marks start/end of build |
| **Cyan/Blue** | The exact PyInstaller command being run |
| **Grey** | Path info (Python, script, output folder) |
| **White** | Normal PyInstaller progress output |
| **Green** | Success — build completed, exe confirmed on disk |
| **Orange** | Warning — build finished but something needs attention |
| **Red** | Error — build failed, read this carefully |

### Reading the Log

```
[ 14:32:01 ]  Build started                        ← yellow: started
Python     : C:\Python311\python.exe               ← grey: which python
Script     : C:\projects\myapp.py                  ← grey: your script
Output dir : C:\projects\dist                      ← grey: where exe goes

Command:                                            ← cyan: exact command
  C:\Python311\python.exe -m PyInstaller --onefile ...

INFO: PyInstaller: 6.3.0                           ← white: normal output
INFO: Python: 3.11.4
INFO: Analyzing myapp.py
INFO: Processing module hooks
INFO: Building PKG
INFO: Building EXE

[ 14:32:18 ]  Build succeeded                      ← green: done!
  Executable : C:\projects\dist\myapp.exe
```

If you see **red text**, scroll up to find the **first** red line — that is usually the root cause of the failure.

### Clear Log Button

Click **"Clear Log"** (next to the progress bar) to wipe the log and start fresh. Useful before rebuilding.

---

## 10. After a Successful Build

When the build succeeds:

1. The status bar turns **green**: `Done. myapp.exe --> C:\projects\dist`
2. A **popup** confirms the exe was created and shows its location
3. The **"Open Output Folder"** button appears — click it to open the folder in Explorer
4. Your `.exe` is at: `[output folder]\[scriptname].exe`

### Testing Your EXE

- Double-click it to run
- For best testing, copy the `.exe` to a different machine (or a folder with no Python) and run it there — this confirms it is truly standalone

### Sharing Your EXE

You can send your `.exe` to anyone running Windows. They do **not** need Python installed. Just share the file directly — via USB, email, cloud drive, etc.

---

## 11. Basic Conversion — Step by Step

The fastest path from script to exe:

**Step 1** — Launch the app:
```bash
python py2exe_converter.py
```

**Step 2** — Press any key on the splash screen.

**Step 3** — In **Section 01**, click **Browse** next to "Python Script *" and select your `.py` file.

**Step 4** — Leave all other settings at their defaults (One-File checked, Windowed unchecked).

**Step 5** — Check **Section 04** — confirm it shows a green Python path.

**Step 6** — Click **CONVERT .py --> .exe**.

**Step 7** — Watch the Build Log. Wait for the green success message (10–90 seconds depending on your script).

**Step 8** — Click **"Open Output Folder"** and find your `.exe`.

**Done.** Your script is now a standalone executable.

---

## 12. Advanced Conversion — Step by Step

### Converting a GUI App (no terminal window)

1. Select your `.py` script in Section 01
2. In **Section 02**, check **"Windowed"**
3. Optionally add an icon in Section 01
4. Press CONVERT
5. The resulting `.exe` will open with no black console window

### Bundling a Script That Reads External Files

Suppose your script reads `config.json` and `logo.png`:

1. Add these lines to your script:
   ```python
   import sys, os
   def res(name):
       base = sys._MEIPASS if getattr(sys,'frozen',False) else os.path.dirname(__file__)
       return os.path.join(base, name)
   # Then use:  open(res("config.json"))  and  res("logo.png")
   ```
2. In **Section 03**, click **+ Add** and select `config.json` and `logo.png`
3. Press CONVERT — both files will be bundled inside the exe

### Using a Custom Icon

1. Prepare a `.ico` file (at least 256×256 pixels recommended)
2. In **Section 01**, click **Browse** next to "Icon (.ico)"
3. Select your `.ico` file
4. Press CONVERT — the icon is embedded in the exe

### Building to a Specific Output Folder

1. In **Section 01**, click **Browse** next to "Output Folder"
2. Select any folder on your system (e.g. `C:\Releases\v1.0\`)
3. The exe will be saved there

### Using a Virtual Environment's Python

If your script uses packages installed in a venv:

1. In **Section 04**, click **Change**
2. Browse to: `C:\your-project\venv\Scripts\python.exe`
3. Press CONVERT — PyInstaller will use that venv's packages

---

## 13. Common Errors and How to Fix Them

### "ModuleNotFoundError: No module named 'xyz'"

Your script uses a package that PyInstaller couldn't auto-detect.

**Fix:**
```bash
pip install xyz
```
Make sure the package is installed for the Python shown in Section 04. Then rebuild.

If it still fails, add this line anywhere in your script:
```python
import xyz  # noqa — tell PyInstaller this import exists
```

---

### "FileNotFoundError: config.json"

Your script tries to read a file that wasn't bundled.

**Fix:** Add the file using Section 03, and update your code to use `sys._MEIPASS` (see Section 6 above).

---

### Build succeeds but exe crashes immediately with no error

This happens in Windowed mode — the error appears but the window closes too fast to see it.

**Fix:** Build in **Console mode** (uncheck Windowed). Run the exe in a terminal:
```bash
cd C:\your\dist\folder
myapp.exe
```
You'll see the full error message. Fix it, then switch back to Windowed.

---

### Antivirus deletes the exe right after build

**Fix:**
1. Open Windows Security
2. Go to Virus & threat protection → Manage settings
3. Scroll to Exclusions → Add or remove exclusions
4. Add your output folder
5. Rebuild

---

### "The application failed to start because no Qt platform plugin could be initialized"

Happens with PyQt5, PyQt6, or PySide apps.

**Fix:** Make sure you are using One-Folder mode (not One-File). Qt apps frequently need their platform plugins in the folder structure.

---

### Build takes forever / appears frozen

Large scripts with many dependencies (scientific computing, ML frameworks) can take 5–10 minutes. The Build Log will still be updating — don't close the app.

---

### PyToExe itself crashes when I press CONVERT

Usually means the Python interpreter in Section 04 is wrong or missing.

**Fix:** Click **Change** in Section 04 and manually point to a working `python.exe`. Then confirm PyInstaller is installed for that Python:
```bash
C:\path\to\python.exe -m pip install pyinstaller
```

---

## 14. Pro Tips

**Always test your script before converting.**
Run `python yourscript.py` first. If it has any errors or crashes as a `.py`, the `.exe` will have the same problems.

**Use Console mode for debugging.**
Always build with Console mode first. Once it works, switch to Windowed. This saves hours of confusion.

**Keep your script in its own folder.**
Put your `.py` and all its related data files in a dedicated folder. This keeps the `dist/` output clean and makes Section 03 bundling straightforward.

**Use a virtual environment for clean builds.**
Activate your venv before building, or point Section 04 to the venv's Python. This keeps the exe small by only including the packages your script actually needs.

**One-Folder is easier to debug.**
If something goes wrong, One-Folder mode lets you inspect exactly what was bundled and what is missing. Switch to One-File once everything works.

**The first red line in the log is the root cause.**
When a build fails, scroll up to the first red line in the Build Log. Everything below it is usually a cascade effect. Fix the first error and rebuild.

**Antivirus exclusions are normal.**
Adding your `dist/` folder to antivirus exclusions is standard practice for PyInstaller builds. It is not a security risk — you are excluding a folder you fully control.

---

<div align="center">

Instagram [@x404ctl](https://instagram.com/x404ctl) &nbsp;|&nbsp; GitHub [@MAliXCS](https://github.com/MAliXCS)

</div>
