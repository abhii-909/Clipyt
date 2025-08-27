
import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root):
    # Dark theme colors
    DARK_BACKGROUND = "#2b2b2b"
    DARK_FOREGROUND = "#ffffff"
    ACCENT_COLOR = "#007bff"  # A nice blue for accents
    DISABLED_COLOR = "#555555"
    ENTRY_BACKGROUND = "#3c3c3c"

    root.configure(bg=DARK_BACKGROUND)
    root.tk_setPalette(background=DARK_BACKGROUND, foreground=DARK_FOREGROUND,
                       activeBackground=ACCENT_COLOR, activeForeground=DARK_FOREGROUND,
                       highlightBackground=ACCENT_COLOR, highlightForeground=DARK_FOREGROUND)

    style = ttk.Style(root)
    style.theme_use('clam') # Base on clam theme

    # General styles
    style.configure(".", font=("Helvetica", 12), background=DARK_BACKGROUND, foreground=DARK_FOREGROUND)

    # Frame style
    style.configure("TFrame", background=DARK_BACKGROUND)

    # Label style
    style.configure("TLabel", background=DARK_BACKGROUND, foreground=DARK_FOREGROUND)
    style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background=DARK_BACKGROUND, foreground=DARK_FOREGROUND)
    style.configure("Status.TLabel", font=("Helvetica", 14), background=DARK_BACKGROUND, foreground=DARK_FOREGROUND)

    # Entry style
    style.configure("TEntry", fieldbackground=ENTRY_BACKGROUND, foreground=DARK_FOREGROUND,
                    insertcolor=DARK_FOREGROUND, bordercolor=ACCENT_COLOR, lightcolor=ACCENT_COLOR,
                    darkcolor=ACCENT_COLOR)
    style.map("TEntry", background=[("readonly", DISABLED_COLOR)])

    # Button style
    style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10,
                    background=ACCENT_COLOR, foreground=DARK_FOREGROUND,
                    relief="flat", borderwidth=0)
    style.map("TButton",
              background=[("active", ACCENT_COLOR)],
              foreground=[("active", DARK_FOREGROUND)],
              focuscolor=[("!active", ACCENT_COLOR)])

    # Accent Button style (for Extract/Generate PDF)
    style.configure("Accent.TButton", background=ACCENT_COLOR, foreground=DARK_FOREGROUND)
    style.map("Accent.TButton",
              background=[("active", ACCENT_COLOR)],
              foreground=[("active", DARK_FOREGROUND)])

    # Progressbar style
    style.configure("TProgressbar", background=ACCENT_COLOR, troughcolor=ENTRY_BACKGROUND,
                    thickness=15, borderwidth=0, relief="flat")
    style.map("TProgressbar",
              background=[("active", ACCENT_COLOR)])

    # Separator style (if needed later)
    style.configure("TSeparator", background=DISABLED_COLOR)

    return style
