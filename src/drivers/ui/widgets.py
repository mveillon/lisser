import tkinter as tk
from typing import Dict, Any, Callable, List

from src.drivers.ui.styling import ColorScheme, FONT, BORDER
from src.models.types import Root


def frame(root: Root, with_hightlight: bool = True) -> tk.Frame:
    """
    Creates the default tkinter Frame.

    Parameters:
        root (Root): the root Tk or Frame
        with_highlight (bool): whether to include a border

    Returns:
        frame (Frame): the default frame
    """
    kwargs: Dict[str, Any] = {"bg": ColorScheme.BACKGROUND}
    if with_hightlight:
        kwargs |= BORDER
    return tk.Frame(root, **kwargs)


def label(root: Root, text: str) -> tk.Label:
    """
    Creates the default tkinter Label.

    Parameters:
        root (Root): the root Tk or Frame
        text (str): what the label should say

    Returns:
        label (Label): the default Label
    """
    return tk.Label(
        root, text=text, fg=ColorScheme.TEXT, bg=ColorScheme.BACKGROUND, font=FONT
    )


def button(root: Root, text: str, command: Callable[[], None]) -> tk.Button:
    """
    Creates the default tkinter Button.

    Paramters:
        root (Root): the root Tk or Frame
        text (str): the text on the button
        command (Callable): what happens when the button is clicked

    Returns:
        button (Button): the default Button
    """
    bg_normal = ColorScheme.HIGHLIGHT
    bg_hover = ColorScheme.BUTTON_HOVER
    fg_normal = ColorScheme.BUTTON_TEXT
    fg_hover = ColorScheme.TEXT

    res = tk.Button(
        root,
        text=text,
        command=command,
        fg=fg_normal,
        bg=bg_normal,
        font=FONT,
    )

    def reset_color(_: tk.Event) -> None:
        res.config(bg=bg_normal, fg=fg_normal)

    def hover(_: tk.Event) -> None:
        res.config(bg=bg_hover, fg=fg_hover)

    res.bind("<Enter>", hover)
    res.bind("<Leave>", reset_color)

    return res


def entry(root: Root, textvar: tk.StringVar) -> tk.Entry:
    """
    Creates the default Entry.

    Parameters:
        root (Root): the root Tk or Frame
        textvar (StringVar): the variable holding the value of the Entry

    Returns:
        entry (Entry): the default Entry
    """
    return tk.Entry(
        root,
        textvariable=textvar,
        bg=ColorScheme.BACKGROUND,
        fg=ColorScheme.TEXT,
        font=FONT,
    )


def option_menu(root: Root, textvar: tk.StringVar, choices: List[str]) -> tk.OptionMenu:
    """
    Creates an OptionMenu where the user can select any of choices.

    Parameters:
        root (Root): the root Tk or Frame
        textvar (StringVar): the variable holding the selected value
        choices (List[str]): the set of choices available to the user

    Returns:
        option_menu (OptionMenu): the default OptionMenu
    """
    configs: Dict[str, Any] = {
        "bg": ColorScheme.HIGHLIGHT,
        "fg": ColorScheme.BUTTON_TEXT,
        "font": FONT,
        "activebackground": ColorScheme.BUTTON_HOVER,
        "activeforeground": ColorScheme.TEXT,
        "bd": 0,
    }
    res = tk.OptionMenu(
        root,
        textvar,
        *choices,
    )
    res.config(**configs)
    res["menu"].config(**configs)
    res.config(highlightthickness=0)

    return res
