from src.classes.Database import Database
from src.classes.Logger import Logger
from src.types.lessons import StoredClass

grades_database: Database[str] = Database(path = "saves/grades")
logger = Logger()
lessons_database: Database[StoredClass] = Database(path = "saves/lessons")