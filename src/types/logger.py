from enum import Enum

class ColorCodes(Enum):
    Reset = 0
    White = 0
    Red = 31
    Green = 32
    Yellow = 33
    DarkBlue = 34
    Purple = 35
    Cyan = 36
    LightRed = 91
    LightGreen = 92
    LightYellow = 93
    LightBlue = 94
    LightPurple = 95
    LightCyan = 96
    LightGrey = 90
    RedBackground = 41
    GreenBackground = 42
    YellowBackground = 43
    DarkBlueBackground = 44
    PurpleBackground = 45
    CyanBackground = 46
    LightGreyBackground = 100
    LightRedBackground = 101
    LightGreenBackground = 102
    LightYellowBackground = 103
    LightBlueBackground = 104
    LightPurpleBackground = 105
    LightCyanBackground = 106
    Underline = 37
    Blink = 5
    Overline = 9
    DoubleUnderline = 21

class LogLevels(Enum):
    Error = ColorCodes.Red
    Warn = ColorCodes.Yellow
    Info = ColorCodes.Cyan
    Debug = ColorCodes.LightGrey
    Success = ColorCodes.Green