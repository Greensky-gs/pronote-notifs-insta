from json import load, dump
from typing import TypeVar, Generic, List, Callable

from src.classes.Logger import Logger
from src.types.logger import LogLevels, ColorCodes
from src.utils.methods import check_saves

local_logger = Logger()

K = TypeVar("K")
class Database(Generic[K]):
    _path: str
    _name: str
    _data: List[K] = list()
    _bulking: bool = False

    def __init__(self, *, path: str = "db"):
        self._path = path + ".json"
        self._name = path
        self._data = []

        self._load()

    def bulk(self):
        self._bulking = True

    def _load(self):
        local_logger.log("Database", LogLevels.Debug, f"Loading database {Logger.chalk(ColorCodes.Red, self._name)}")

        check_saves()

        try:
            with open(self._path, "r") as file:
                self._data = load(file)

                local_logger.log("Database", LogLevels.Success, f"Database {Logger.chalk(ColorCodes.Red, self._name)} loaded ({Logger.chalk(ColorCodes.Red, str(len(self._data)))} keys)")
        except FileNotFoundError:
            local_logger.log("Database", LogLevels.Warn, f"Database {Logger.chalk(ColorCodes.Red, self._name)} not found")

    def apply_filter(self, filter_func: Callable[[K], bool]):
        local_logger.log("Database", LogLevels.Debug, f"Applying filter to database {Logger.chalk(ColorCodes.Red, self._name)}")
        self._data = list(filter(filter_func, self._data))

        self._save()
    @property
    def data(self):
        return self._data[:]

    def unbulk(self):
        self._bulking = False

        local_logger.log("Database", LogLevels.Debug, f"Unbulking database {Logger.chalk(ColorCodes.Red, self._name)}")
        self._save()

    def _save(self):
        if self._bulking:
            return

        local_logger.log("Database", LogLevels.Debug, f"Saving database {Logger.chalk(ColorCodes.Red, self._name)}")

        with open(self._path, "w") as file:
            dump(self._data, file, indent=4)

            local_logger.log("Database", LogLevels.Success, f"Database {Logger.chalk(ColorCodes.Red, self._name)} saved")

    def append_datas(self, datas: List[K]):
        self._data.extend(datas)

        self._save()

    def remove_data(self, data: K):
        self._data.remove(data)

        self._save()

    def append_data(self, data: K):
        self._data.append(data)

        self._save()