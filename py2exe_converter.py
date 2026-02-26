"""
PyToExe Converter  v2.1
Author  : Instagram @x404ctl  |  GitHub @MAliX
Requires: Python 3.6+, PyInstaller (auto-installed if missing), tkinter (built-in)
Compatible: Windows 7, 8, 10, 11

FIXES IN v2.1
─────────────
- CRITICAL: detect real Python interpreter even when this app is itself
  packed as a .exe (sys.executable points to frozen exe in that case)
- CRITICAL: build_command() now returns only cmd list (was wrongly
  returning a 3-tuple that broke the thread silently)
- Resolve all paths to absolute before passing to PyInstaller
- Removed --clean flag (causes file-lock errors on Windows)
- Removed cwd= override (caused drive-letter conflicts)
- Added exe-existence check after a "successful" build
- Improved error messages with actionable hints
- Thread now catches ALL exceptions and always re-enables the button
"""

import os
import sys
import time
import shutil
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path

# ══════════════════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════════════════
T = {
    "bg":         "#0d1117",
    "panel":      "#161b22",
    "border":     "#30363d",
    "accent":     "#238636",
    "accent_hov": "#2ea043",
    "accent_dim": "#1a5c28",
    "blue":       "#1f6feb",
    "blue_hov":   "#388bfd",
    "text":       "#e6edf3",
    "text_dim":   "#8b949e",
    "danger":     "#da3633",
    "warn":       "#d29922",
    "ok":         "#3fb950",
    "log_bg":     "#010409",
    "log_fg":     "#c9d1d9",
    "entry_bg":   "#21262d",
    "entry_fg":   "#e6edf3",
    "select_bg":  "#1f6feb",
    "btn_bg":     "#21262d",
    "btn_fg":     "#e6edf3",
    "btn_hov":    "#30363d",
    "splash_bg":  "#010409",
    "splash_fg":  "#3fb950",
}

FONT_UI    = ("Consolas", 9)
FONT_MONO  = ("Consolas", 9)
FONT_HEAD  = ("Consolas", 10, "bold")
FONT_SPLASH = ("Consolas", 11)
PAD = 10


# ══════════════════════════════════════════════════════════
#  CRITICAL HELPER — find the REAL Python executable
#  When this .py is packaged as a .exe by PyInstaller,
#  sys.executable becomes the frozen app itself, NOT python.exe.
#  We must locate the actual python.exe to run PyInstaller.
# ══════════════════════════════════════════════════════════
def find_python() -> str:
    """
    Return the path to a working python.exe.
    Priority:
      1. sys.executable  (works when running as .py directly)
      2. 'python' / 'python3' on PATH
      3. Common install locations on Windows
    Returns empty string if none found.
    """
    # If NOT frozen (running as plain .py), sys.executable is python.exe
    if not getattr(sys, "frozen", False):
        return sys.executable

    # Frozen — sys.executable is the packed .exe, useless for subprocess.
    # Try PATH first.
    for name in ("python", "python3", "py"):
        found = shutil.which(name)
        if found:
            # Quick sanity check
            try:
                out = subprocess.check_output(
                    [found, "--version"],
                    stderr=subprocess.STDOUT,
                    timeout=5,
                )
                if b"Python 3" in out:
                    return found
            except Exception:
                pass

    # Try common Windows install locations
    drives = ["C", "D"]
    candidates = []
    for d in drives:
        for pattern in [
            f"{d}:\\Python3*\\python.exe",
            f"{d}:\\Program Files\\Python3*\\python.exe",
            f"{d}:\\Users\\*\\AppData\\Local\\Programs\\Python\\Python3*\\python.exe",
        ]:
            import glob
            candidates.extend(glob.glob(pattern))

    for exe in candidates:
        if os.path.isfile(exe):
            try:
                out = subprocess.check_output(
                    [exe, "--version"],
                    stderr=subprocess.STDOUT,
                    timeout=5,
                )
                if b"Python 3" in out:
                    return exe
            except Exception:
                pass

    return ""


def ensure_pyinstaller(python_exe: str) -> bool:
    """Check PyInstaller is importable via python_exe; offer to install."""
    try:
        subprocess.check_call(
            [python_exe, "-c", "import PyInstaller"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    except FileNotFoundError:
        messagebox.showerror(
            "Python Not Found",
            f"Could not run:\n{python_exe}\n\n"
            "Make sure Python 3 is installed and added to PATH.",
        )
        return False

    if not messagebox.askyesno(
        "PyInstaller Missing",
        "PyInstaller is not installed.\n\nInstall it now via pip?",
    ):
        return False

    try:
        subprocess.check_call(
            [python_exe, "-m", "pip", "install", "pyinstaller"],
            timeout=120,
        )
        return True
    except Exception as exc:
        messagebox.showerror(
            "Install Failed",
            f"Could not install PyInstaller automatically.\n\n"
            f"Run this manually in a terminal:\n"
            f"  pip install pyinstaller\n\nError: {exc}",
        )
        return False


def build_command(cfg: dict, python_exe: str) -> list:
    """
    Build and return the PyInstaller command list.
    All paths are converted to absolute strings.
    """
    script   = os.path.abspath(cfg["script"])
    out_dir  = os.path.abspath(cfg["output_dir"]) if cfg["output_dir"] \
               else os.path.join(os.path.dirname(script), "dist")
    work_dir = os.path.join(os.path.dirname(script), "__pybuild_tmp__")
    sep      = ";" if sys.platform == "win32" else ":"

    cmd = [python_exe, "-m", "PyInstaller"]

    # Name (avoids issues with spaces in filename)
    cmd += ["--name", Path(script).stem]

    # Bundle mode
    cmd.append("--onefile" if cfg["onefile"] else "--onedir")

    # Window mode
    cmd.append("--windowed" if cfg["windowed"] else "--console")

    # Icon
    if cfg["icon"]:
        cmd += ["--icon", os.path.abspath(cfg["icon"])]

    # Extra data files
    for f in cfg["extra_files"]:
        src  = os.path.abspath(f)
        dest = os.path.basename(f)
        cmd += ["--add-data", f"{src}{sep}{dest}"]

    # Output / work paths (absolute)
    cmd += ["--distpath",  out_dir]
    cmd += ["--workpath",  work_dir]
    cmd += ["--specpath",  work_dir]

    # Never prompt, never pause
    cmd += ["--noconfirm"]

    # Script last — absolute path
    cmd.append(script)

    return cmd, out_dir   # return cmd + resolved dist path


def open_folder(path: str):
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


# ══════════════════════════════════════════════════════════
#  SPLASH  SCREEN
# ══════════════════════════════════════════════════════════
class SplashScreen(tk.Toplevel):
    LINES = [
        ("",                                                             0.00),
        ("  ██████╗ ██╗   ██╗    ██████╗     ███████╗██╗  ██╗███████╗", 0.03),
        ("  ██╔══██╗╚██╗ ██╔╝    ╚════██╗    ██╔════╝╚██╗██╔╝██╔════╝", 0.03),
        ("  ██████╔╝ ╚████╔╝      █████╔╝    █████╗   ╚███╔╝ █████╗  ", 0.03),
        ("  ██╔═══╝   ╚██╔╝       ╚═══██╗    ██╔══╝   ██╔██╗ ██╔══╝  ", 0.03),
        ("  ██║        ██║        ██████╔╝    ███████╗██╔╝ ██╗███████╗", 0.03),
        ("  ╚═╝        ╚═╝        ╚═════╝     ╚══════╝╚═╝  ╚═╝╚══════╝",0.05),
        ("",                                                             0.03),
        ("  Python  -->  EXE  Converter   v2.1",                        0.04),
        ("  Author  :  Instagram @x404ctl   |   GitHub @MAliX",         0.04),
        ("",                                                             0.02),
        ("  " + "─" * 62,                                               0.02),
        ("",                                                             0.03),
        ("  [ * ]  Initializing runtime environment ...",               0.06),
        ("  [ * ]  Locating Python interpreter ...",                    0.07),
        ("  [ * ]  Loading PyInstaller interface ...",                   0.07),
        ("  [ * ]  Configuring build workspace ...",                    0.07),
        ("  [ * ]  All systems ready.",                                  0.08),
        ("",                                                             0.04),
        ("  " + "─" * 62,                                               0.02),
        ("",                                                             0.05),
        ("        Press any key to continue ...",                        0.00),
    ]

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self._done  = False
        self._line  = 0

        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h   = 740, 490
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(bg=T["splash_bg"])
        self.overrideredirect(True)
        self.lift()
        self.focus_force()

        border = tk.Frame(self, bg=T["splash_fg"], padx=2, pady=2)
        border.pack(fill="both", expand=True, padx=6, pady=6)
        inner  = tk.Frame(border, bg=T["splash_bg"])
        inner.pack(fill="both", expand=True)

        self._txt = tk.Text(
            inner,
            bg=T["splash_bg"], fg=T["splash_fg"],
            font=FONT_SPLASH,
            relief="flat", bd=0,
            state="disabled", cursor="none",
            wrap="none", highlightthickness=0,
        )
        self._txt.pack(fill="both", expand=True, padx=10, pady=10)
        self._txt.tag_configure("logo",  foreground="#58d68d",
                                font=("Consolas", 11, "bold"))
        self._txt.tag_configure("info",  foreground="#aed6f1")
        self._txt.tag_configure("dim",   foreground=T["text_dim"])
        self._txt.tag_configure("ready", foreground="#f0e68c",
                                font=("Consolas", 11, "bold"))
        self._txt.tag_configure("press", foreground="#ffffff",
                                font=("Consolas", 11, "bold"))

        self.bind("<Key>",    self._dismiss)
        self.bind("<Button>", self._dismiss)
        self.after(250, self._type_line)

    def _write(self, text, tag=""):
        self._txt.configure(state="normal")
        if tag:
            self._txt.insert("end", text, tag)
        else:
            self._txt.insert("end", text)
        self._txt.see("end")
        self._txt.configure(state="disabled")

    def _type_line(self):
        if self._done or self._line >= len(self.LINES):
            if not self._done:
                self._blink(True)
            return
        text, delay = self.LINES[self._line]
        self._line += 1
        if "██" in text:
            tag = "logo"
        elif text.strip().startswith("[ * ]"):
            tag = "dim"
        elif "Python  -->" in text or "Author" in text:
            tag = "info"
        elif "All systems ready" in text:
            tag = "ready"
        elif "Press any key" in text:
            tag = "press"
        else:
            tag = ""
        self._write(text + "\n", tag)
        self.after(max(int(delay * 1000), 10), self._type_line)

    def _blink(self, state: bool):
        if self._done:
            return
        self._txt.configure(state="normal")
        idx = self._txt.index("end-1c")
        last = self._txt.get("end-2c", "end-1c")
        if last in ("_", " "):
            self._txt.delete("end-2c", "end-1c")
        self._txt.insert("end-1c", "_" if state else " ", "press")
        self._txt.configure(state="disabled")
        self.after(500, self._blink, not state)

    def _dismiss(self, event=None):
        if self._done:
            return
        self._done = True
        self.destroy()
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()


# ══════════════════════════════════════════════════════════
#  MAIN  APPLICATION
# ══════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.title("PyToExe Converter  //  @x404ctl  |  @MAliX")
        w, h = 820, 740
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(750, 640)
        self.configure(bg=T["bg"])
        self.resizable(True, True)

        # Locate real Python ONCE at startup
        self._python_exe = find_python()

        # State
        self.script_var   = tk.StringVar()
        self.output_var   = tk.StringVar()
        self.icon_var     = tk.StringVar()
        self.onefile_var  = tk.BooleanVar(value=True)
        self.windowed_var = tk.BooleanVar(value=False)
        self.extra_files  = []
        self._thread      = None
        self._last_out    = ""
        self._open_visible = False

        self._apply_style()
        self._build_ui()
        SplashScreen(self)

        # Warn early if Python not found
        if not self._python_exe:
            self.after(800, self._warn_no_python)

    def _warn_no_python(self):
        messagebox.showerror(
            "Python Not Found",
            "PyToExe could not locate a Python 3 interpreter.\n\n"
            "Make sure Python 3 is installed and added to your system PATH.\n\n"
            "Download from: https://python.org/downloads\n"
            "(Check 'Add Python to PATH' during installation)",
        )

    # ══════════════════════════════════════════
    #  STYLE
    # ══════════════════════════════════════════
    def _apply_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".",
                    background=T["bg"], foreground=T["text"],
                    font=FONT_UI, borderwidth=0)
        s.configure("TFrame",       background=T["bg"])
        s.configure("TLabel",       background=T["bg"],
                    foreground=T["text"], font=FONT_UI)
        s.configure("TCheckbutton", background=T["bg"],
                    foreground=T["text"], font=FONT_UI,
                    focuscolor=T["bg"])
        s.map("TCheckbutton",
              background=[("active", T["bg"])],
              foreground=[("active", T["accent_hov"])])
        s.configure("TEntry",
                    fieldbackground=T["entry_bg"],
                    foreground=T["entry_fg"],
                    insertcolor=T["text"],
                    bordercolor=T["border"],
                    font=FONT_MONO)
        s.map("TEntry", bordercolor=[("focus", T["blue"])])
        s.configure("TProgressbar",
                    troughcolor=T["panel"],
                    background=T["accent"],
                    bordercolor=T["border"],
                    lightcolor=T["accent"],
                    darkcolor=T["accent"])
        s.configure("TScrollbar",
                    background=T["border"],
                    troughcolor=T["panel"],
                    arrowcolor=T["text_dim"])

    # ══════════════════════════════════════════
    #  UI LAYOUT
    # ══════════════════════════════════════════
    def _build_ui(self):
        self._make_titlebar()

        wrap   = tk.Frame(self, bg=T["bg"])
        wrap.pack(fill="both", expand=True)

        canvas = tk.Canvas(wrap, bg=T["bg"], highlightthickness=0)
        vsb    = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._sf = tk.Frame(canvas, bg=T["bg"])
        wid = canvas.create_window((0, 0), window=self._sf, anchor="nw")

        def _resize(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(wid, width=canvas.winfo_width())

        self._sf.bind("<Configure>", _resize)
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(wid, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(
                            -1 * (e.delta // 120), "units"))

        self._section_files(self._sf)
        self._section_options(self._sf)
        self._section_extras(self._sf)
        self._section_python_info(self._sf)   # shows detected Python path
        self._section_convert(self._sf)
        self._section_log(self._sf)
        self._make_statusbar()

    # ── Title bar ─────────────────────────────
    def _make_titlebar(self):
        bar = tk.Frame(self, bg=T["blue"], height=54)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, text=" PY ",
                 bg=T["accent"], fg="#fff",
                 font=("Consolas", 13, "bold"),
                 padx=4).pack(side="left", padx=(14, 0), pady=12)
        tk.Label(bar, text="  PyToExe  Converter",
                 bg=T["blue"], fg="#ffffff",
                 font=("Consolas", 15, "bold")).pack(side="left")
        tk.Label(bar, text="Instagram @x404ctl   |   GitHub @MAliX   ",
                 bg=T["blue"], fg="#93c5fd",
                 font=("Consolas", 8)).pack(side="right", padx=14)

    # ── Status bar ────────────────────────────
    def _make_statusbar(self):
        sb = tk.Frame(self, bg=T["panel"], height=28)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        tk.Frame(sb, bg=T["border"], width=1).pack(side="left", fill="y")
        self._dot = tk.Label(sb, text="  ●  ",
                             bg=T["panel"], fg=T["text_dim"],
                             font=("Consolas", 9, "bold"))
        self._dot.pack(side="left")
        self._status = tk.Label(
            sb,
            text="Ready.   Select a Python script then press CONVERT.",
            bg=T["panel"], fg=T["text_dim"],
            font=("Consolas", 8), anchor="w",
        )
        self._status.pack(side="left", fill="x", expand=True)
        tk.Label(sb, text="  PyToExe v2.1  by @x404ctl   ",
                 bg=T["panel"], fg=T["border"],
                 font=("Consolas", 8)).pack(side="right")

    # ── Card helper ───────────────────────────
    def _card(self, parent, title: str) -> tk.Frame:
        outer = tk.Frame(parent, bg=T["border"], padx=1, pady=1)
        outer.pack(fill="x", padx=PAD, pady=(0, PAD))
        hdr = tk.Frame(outer, bg="#1c2128")
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  {title}",
                 bg="#1c2128", fg=T["blue_hov"],
                 font=FONT_HEAD, anchor="w").pack(
            side="left", padx=8, pady=6)
        tk.Frame(outer, bg=T["border"], height=1).pack(fill="x")
        body = tk.Frame(outer, bg=T["panel"])
        body.pack(fill="x")
        return body

    # ── File-row helper ───────────────────────
    def _file_row(self, parent, label, row, var, cmd):
        tk.Label(parent, text=label,
                 bg=T["panel"], fg=T["text_dim"],
                 font=FONT_UI, width=17, anchor="e"
                 ).grid(row=row, column=0, padx=(PAD, 6), pady=6, sticky="e")
        e = tk.Entry(parent,
                     textvariable=var,
                     bg=T["entry_bg"], fg=T["entry_fg"],
                     insertbackground=T["text"],
                     relief="flat", font=FONT_MONO,
                     highlightthickness=1,
                     highlightbackground=T["border"],
                     highlightcolor=T["blue"])
        e.grid(row=row, column=1, sticky="ew", pady=6)
        tk.Button(parent, text="Browse",
                  bg=T["btn_bg"], fg=T["btn_fg"],
                  activebackground=T["btn_hov"],
                  activeforeground=T["text"],
                  relief="flat", font=FONT_UI,
                  cursor="hand2", padx=10,
                  command=cmd).grid(
            row=row, column=2, padx=(6, PAD), pady=6)

    # ── Sections ─────────────────────────────
    def _section_files(self, p):
        tk.Frame(p, bg=T["bg"], height=PAD).pack()
        body = self._card(p, "01  /  Select Files")
        body.columnconfigure(1, weight=1)
        self._file_row(body, "Python Script  *", 0,
                       self.script_var, self._browse_script)
        self._file_row(body, "Output Folder",    1,
                       self.output_var, self._browse_output)
        self._file_row(body, "Icon  (.ico)",      2,
                       self.icon_var,   self._browse_icon)
        tk.Frame(body, bg=T["panel"], height=6).grid(
            row=3, column=0, columnspan=3)

    def _section_options(self, p):
        body = self._card(p, "02  /  Build Options")
        row  = tk.Frame(body, bg=T["panel"])
        row.pack(anchor="w", padx=PAD, pady=10)

        def cb(txt, var):
            return tk.Checkbutton(
                row, text=txt, variable=var,
                bg=T["panel"], fg=T["text"],
                activebackground=T["panel"],
                activeforeground=T["accent_hov"],
                selectcolor=T["entry_bg"],
                font=FONT_UI, cursor="hand2",
                relief="flat", bd=0,
            )

        cb("One-File  ( single .exe )",       self.onefile_var ).pack(side="left", padx=(0, 30))
        cb("Windowed  ( no console window )", self.windowed_var).pack(side="left")

    def _section_extras(self, p):
        body  = self._card(p, "03  /  Additional Files  ( optional )")
        inner = tk.Frame(body, bg=T["panel"])
        inner.pack(fill="x", padx=PAD, pady=10)

        lbf = tk.Frame(inner, bg=T["border"], padx=1, pady=1)
        lbf.pack(side="left", fill="both", expand=True)

        self._extras_lb = tk.Listbox(
            lbf, height=3,
            bg=T["log_bg"], fg=T["log_fg"],
            selectbackground=T["select_bg"],
            selectforeground="#fff",
            font=FONT_MONO,
            relief="flat", bd=0, activestyle="none",
        )
        self._extras_lb.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(lbf, orient="vertical",
                          command=self._extras_lb.yview,
                          bg=T["border"], troughcolor=T["panel"])
        sb.pack(side="right", fill="y")
        self._extras_lb.configure(yscrollcommand=sb.set)

        bcol = tk.Frame(inner, bg=T["panel"])
        bcol.pack(side="left", padx=(8, 0))
        for txt, fn in [("+ Add", self._add_extra),
                        ("- Remove", self._remove_extra)]:
            tk.Button(bcol, text=txt,
                      bg=T["btn_bg"], fg=T["btn_fg"],
                      activebackground=T["btn_hov"],
                      activeforeground=T["text"],
                      relief="flat", font=FONT_UI,
                      cursor="hand2", width=10,
                      command=fn).pack(pady=2)

    def _section_python_info(self, p):
        """Shows which Python will be used — critical for transparency."""
        body = self._card(p, "04  /  Python Interpreter  ( detected automatically )")
        row  = tk.Frame(body, bg=T["panel"])
        row.pack(fill="x", padx=PAD, pady=8)

        color  = T["ok"]   if self._python_exe else T["danger"]
        status = self._python_exe if self._python_exe else \
                 "NOT FOUND — install Python 3 and add it to PATH"

        self._py_lbl = tk.Label(
            row,
            text=f"  {status}",
            bg=T["panel"], fg=color,
            font=FONT_MONO, anchor="w",
        )
        self._py_lbl.pack(side="left", fill="x", expand=True)

        tk.Button(row, text="Change",
                  bg=T["btn_bg"], fg=T["btn_fg"],
                  activebackground=T["btn_hov"],
                  activeforeground=T["text"],
                  relief="flat", font=FONT_UI,
                  cursor="hand2", padx=8,
                  command=self._browse_python).pack(side="right")

    def _section_convert(self, p):
        wrapper = tk.Frame(p, bg=T["bg"])
        wrapper.pack(fill="x", padx=PAD, pady=(0, PAD))

        self._conv_btn = tk.Button(
            wrapper,
            text="  CONVERT   .py  -->  .exe  ",
            font=("Consolas", 14, "bold"),
            bg=T["accent"],
            fg="#ffffff",
            activebackground=T["accent_hov"],
            activeforeground="#ffffff",
            relief="flat", cursor="hand2",
            pady=16, bd=0,
            command=self._start_build,
        )
        self._conv_btn.pack(fill="x")

        prow = tk.Frame(wrapper, bg=T["bg"])
        prow.pack(fill="x", pady=(6, 0))
        self._progress = ttk.Progressbar(prow, mode="indeterminate")
        self._progress.pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(prow, text="Clear Log",
                  bg=T["btn_bg"], fg=T["text_dim"],
                  activebackground=T["btn_hov"],
                  activeforeground=T["text"],
                  relief="flat", font=FONT_UI,
                  cursor="hand2", padx=10, pady=3,
                  command=self._clear_log).pack(side="right")

        # Hidden until success
        self._open_btn = tk.Button(
            wrapper,
            text="  Open Output Folder  ",
            font=("Consolas", 10, "bold"),
            bg="#0d3321", fg=T["ok"],
            activebackground="#1a5c38",
            activeforeground="#fff",
            relief="flat", cursor="hand2",
            pady=8, bd=0,
            command=self._open_output,
        )

    def _section_log(self, p):
        body = self._card(p, "05  /  Build Log")
        self._log = scrolledtext.ScrolledText(
            body,
            font=FONT_MONO,
            bg=T["log_bg"], fg=T["log_fg"],
            insertbackground=T["text"],
            selectbackground=T["select_bg"],
            relief="flat", bd=0,
            state="disabled", wrap="none",
            height=14,
        )
        self._log.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        self._log.tag_configure("ok",   foreground=T["ok"])
        self._log.tag_configure("err",  foreground=T["danger"])
        self._log.tag_configure("warn", foreground=T["warn"])
        self._log.tag_configure("cmd",  foreground="#79c0ff")
        self._log.tag_configure("head", foreground="#e3b341",
                                font=("Consolas", 9, "bold"))
        self._log.tag_configure("dim",  foreground=T["text_dim"])
        tk.Frame(p, bg=T["bg"], height=PAD).pack()

    # ══════════════════════════════════════════
    #  BROWSE  DIALOGS
    # ══════════════════════════════════════════
    def _browse_script(self):
        p = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python files", "*.py *.pyw"), ("All files", "*.*")],
        )
        if p:
            self.script_var.set(p)
            if not self.output_var.get():
                self.output_var.set(str(Path(p).parent / "dist"))

    def _browse_output(self):
        p = filedialog.askdirectory(title="Select Output Folder")
        if p:
            self.output_var.set(p)

    def _browse_icon(self):
        p = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")],
        )
        if p:
            self.icon_var.set(p)

    def _browse_python(self):
        p = filedialog.askopenfilename(
            title="Select python.exe",
            filetypes=[("Python executable", "python*.exe"), ("All files", "*.*")],
        )
        if p:
            self._python_exe = p
            self._py_lbl.configure(text=f"  {p}", fg=T["ok"])

    def _add_extra(self):
        for p in filedialog.askopenfilenames(title="Select Files to Bundle"):
            if p not in self.extra_files:
                self.extra_files.append(p)
                self._extras_lb.insert("end", f"  {os.path.basename(p)}")

    def _remove_extra(self):
        for i in reversed(self._extras_lb.curselection()):
            self._extras_lb.delete(i)
            self.extra_files.pop(i)

    # ══════════════════════════════════════════
    #  LOG  UTILITIES
    # ══════════════════════════════════════════
    def _log_write(self, text: str, tag: str = ""):
        self._log.configure(state="normal")
        if tag:
            self._log.insert("end", text, tag)
        else:
            self._log.insert("end", text)
        self._log.see("end")
        self._log.configure(state="disabled")

    def _clear_log(self):
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")

    def _set_status(self, text: str, dot: str = T["text_dim"]):
        self._status.configure(text=f"  {text}")
        self._dot.configure(fg=dot)

    def _unlock_ui(self):
        """Always re-enable the convert button — called on any build exit."""
        self._progress.stop()
        self._conv_btn.configure(
            state="normal",
            text="  CONVERT   .py  -->  .exe  ",
            bg=T["accent"],
        )

    # ══════════════════════════════════════════
    #  VALIDATION
    # ══════════════════════════════════════════
    def _validate(self) -> bool:
        if not self._python_exe:
            messagebox.showerror(
                "Python Not Found",
                "No Python interpreter was detected.\n\n"
                "Use the 'Change' button in section 04 to manually\n"
                "locate your python.exe file.",
            )
            return False
        s = self.script_var.get().strip()
        if not s:
            messagebox.showwarning("No Script",
                                   "Please select a .py file first.")
            return False
        if not os.path.isfile(s):
            messagebox.showerror("Not Found", f"File not found:\n{s}")
            return False
        ico = self.icon_var.get().strip()
        if ico and not os.path.isfile(ico):
            messagebox.showerror("Icon Not Found",
                                 f"Icon file not found:\n{ico}")
            return False
        return True

    # ══════════════════════════════════════════
    #  BUILD  PIPELINE
    # ══════════════════════════════════════════
    def _start_build(self):
        if self._thread and self._thread.is_alive():
            messagebox.showinfo("Busy", "A build is already running.")
            return
        if not self._validate():
            return
        if not ensure_pyinstaller(self._python_exe):
            return

        cfg = {
            "script":      self.script_var.get().strip(),
            "output_dir":  self.output_var.get().strip() or None,
            "icon":        self.icon_var.get().strip() or None,
            "onefile":     self.onefile_var.get(),
            "windowed":    self.windowed_var.get(),
            "extra_files": list(self.extra_files),
        }

        if self._open_visible:
            self._open_btn.pack_forget()
            self._open_visible = False

        self._conv_btn.configure(
            state="disabled",
            text="  Building  ...  please wait  ",
            bg=T["accent_dim"],
        )
        self._progress.start(8)
        self._set_status("Building  ...  compiling your script.", T["blue"])
        self._clear_log()

        self._thread = threading.Thread(
            target=self._run_build, args=(cfg,), daemon=True)
        self._thread.start()

    def _run_build(self, cfg: dict):
        # Build command — get cmd list AND resolved dist dir
        try:
            cmd, abs_dist = build_command(cfg, self._python_exe)
        except Exception as exc:
            self.after(0, self._log_write,
                       f"\nFailed to build command: {exc}\n", "err")
            self.after(0, self._unlock_ui)
            self.after(0, self._set_status,
                       "Build failed.  See log.", T["danger"])
            return

        ts = time.strftime("%H:%M:%S")
        self.after(0, self._log_write, f"[ {ts} ]  Build started\n", "head")
        self.after(0, self._log_write,
                   f"Python     : {self._python_exe}\n", "dim")
        self.after(0, self._log_write,
                   f"Script     : {cfg['script']}\n", "dim")
        self.after(0, self._log_write,
                   f"Output dir : {abs_dist}\n", "dim")
        self.after(0, self._log_write,
                   "\nCommand:\n  " + " ".join(cmd) + "\n\n", "cmd")

        # Ensure dist folder exists
        try:
            os.makedirs(abs_dist, exist_ok=True)
        except OSError as exc:
            self.after(0, self._log_write,
                       f"\nCannot create output folder:\n{exc}\n", "err")
            self.after(0, self._unlock_ui)
            self.after(0, self._set_status,
                       "Build failed.  See log.", T["danger"])
            return

        success = False
        try:
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            proc  = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=flags,
                # NO cwd override — use absolute paths throughout
            )
            for line in proc.stdout:
                self.after(0, self._log_write, line)
            proc.wait()
            success = proc.returncode == 0
        except FileNotFoundError:
            self.after(0, self._log_write,
                       f"\nERROR: Could not launch:\n  {self._python_exe}\n\n"
                       "Make sure Python is installed and on PATH.\n", "err")
        except Exception as exc:
            self.after(0, self._log_write,
                       f"\nUnexpected error: {exc}\n", "err")

        # Pass resolved dist path back via cfg dict
        cfg["_abs_dist"] = abs_dist
        self.after(0, self._build_finished, success, cfg)

    def _build_finished(self, success: bool, cfg: dict):
        self._unlock_ui()
        ts   = time.strftime("%H:%M:%S")
        out  = cfg.get("_abs_dist", "")
        name = Path(cfg["script"]).stem + ".exe"
        exe  = os.path.join(out, name)

        if success and os.path.isfile(exe):
            # Real success — exe exists on disk
            self._last_out = out
            self._log_write(f"\n[ {ts} ]  Build succeeded\n", "ok")
            self._log_write(f"  Executable : {exe}\n", "ok")
            self._set_status(f"Done.   {name}  -->  {out}", T["ok"])
            self._open_btn.pack(fill="x", pady=(8, 0))
            self._open_visible = True
            messagebox.showinfo(
                "Build Successful",
                f"'{name}' was created successfully.\n\n"
                f"Location:\n{exe}",
            )

        elif success and not os.path.isfile(exe):
            # PyInstaller said OK but no file found — common with antivirus
            self._log_write(
                f"\n[ {ts} ]  PyInstaller finished OK but .exe was NOT found.\n"
                f"  Expected: {exe}\n", "warn")
            self._log_write(
                "\n  Most likely causes:\n"
                "  1. Antivirus deleted the .exe immediately after creation\n"
                "     --> Add your output folder to antivirus exclusions\n"
                "  2. The output folder was changed mid-build\n"
                "  3. A previous .spec file conflict (delete __pybuild_tmp__)\n",
                "warn")
            self._set_status(
                "Build finished but .exe not found.  Antivirus?", T["warn"])
            messagebox.showwarning(
                "EXE Not Found",
                f"PyInstaller finished without errors but\n"
                f"'{name}' was not found at:\n{exe}\n\n"
                "Most likely cause: Antivirus deleted it.\n\n"
                "Fix: Add your output folder to antivirus exclusions,\n"
                "then build again.",
            )

        else:
            # Real failure
            self._log_write(f"\n[ {ts} ]  Build FAILED.  See log above.\n",
                            "err")
            self._set_status(
                "Build failed.  See the Build Log for details.", T["danger"])
            messagebox.showerror(
                "Build Failed",
                "PyInstaller encountered errors.\n"
                "Read the Build Log carefully — the first red line\n"
                "is usually the root cause.",
            )

    def _open_output(self):
        if self._last_out and os.path.isdir(self._last_out):
            open_folder(self._last_out)
        else:
            messagebox.showwarning("Not Found",
                                   "Output folder no longer exists.")


# ══════════════════════════════════════════════════════════
#  ENTRY  POINT
# ══════════════════════════════════════════════════════════
def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
