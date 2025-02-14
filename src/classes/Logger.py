from datetime import datetime

from src.types.logger import LogLevels, ColorCodes


class Logger:
    def __init__(self):
        pass
    
    def log(self, title: str, level: LogLevels, message: str) -> None:
        """Logs a message with formatted title and colored output."""
        title = title[:17] + "..." if len(title) > 20 else title
        
        timestamp = self.timestamp
        formatted_title = self._blank(20 - len(title))

        console_output = (
            f"{self.chalk(ColorCodes.Purple, timestamp)}"
            f"{self._blank(4)}"
            f"{self.chalk(level.value, title)}"
            f"{formatted_title}"
            f"{message}"
        )
        print(console_output)
    
    @property
    def timestamp(self) -> str:
        """Returns current timestamp in HH:MM:SS format."""
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
    @staticmethod
    def _blank(length: int) -> str:
        """Creates a string of spaces of specified length."""
        return " " * length
    
    @staticmethod
    def chalk(color_code: ColorCodes, text: str) -> str:
        """Applies ANSI color codes to text."""
        return f"\033[{color_code.value}m{text}\033[{ColorCodes.Reset.value}m"