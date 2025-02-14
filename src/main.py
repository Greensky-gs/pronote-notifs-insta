import pronotepy
from dotenv import load_dotenv

from src.cache.data import logger
from src.core.grades import run_grades
from src.core.lessons import run_lessons
from src.types.logger import LogLevels
from src.utils.methods import get_creds, save_creds

load_dotenv()

logger.log("Starting", LogLevels.Info, "Starting script")

logger.log("Creds", LogLevels.Info, "Getting creds")
creds = get_creds()

logger.log("Pronote", LogLevels.Info, "Logging in")
client = pronotepy.Client.token_login(**creds)

logger.log("Pronote", LogLevels.Info, "Exporting creds")
creds = client.export_credentials()

logger.log("Creds", LogLevels.Info, "Saving creds")
save_creds(creds)

run_grades(client)
run_lessons(client)
