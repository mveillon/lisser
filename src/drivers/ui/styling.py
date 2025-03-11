from enum import StrEnum


FONT = ("Corbel Light", 20)
PADDING = 10

class ColorScheme(StrEnum):
    BACKGROUND = "#2a2f38"
    TEXT = "#c2bcb2"
    ACCENT = "#f4dbd8"
    HIGHLIGHT = "#36939e"
    BUTTON_TEXT = "#2d2524"
    BUTTON_HOVER = "#266B72"


BORDER = {
    "highlightbackground": ColorScheme.ACCENT,
    "highlightthickness": 2,
}
