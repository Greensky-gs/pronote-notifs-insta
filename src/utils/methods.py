import json
import os

from src.classes.Logger import Logger
from src.types.logger import LogLevels

logger = Logger()

def check_saves():
    if not os.path.exists("saves"):
        logger.log("Saves", LogLevels.Warn, "saves folder not found, creating it")

        os.mkdir('saves')

        logger.log("Saves", LogLevels.Success, "saves folder created")
def get_creds():
    check_saves()

    try:
        with open('saves/creds.json') as f:
            logger.log("Creds", LogLevels.Info, "creds.json found, using custom creds")
            creds = json.load(f)

            return creds
    except FileNotFoundError:
        logger.log("Creds", LogLevels.Warn, "creds.json not found, raising an error")

        raise FileNotFoundError("creds.json not found")

def save_creds(creds):
    check_saves()

    try:
        with open('saves/creds.json', 'w') as f:
            logger.log("Creds", LogLevels.Info, "Saving creds to creds.json")

            json.dump(creds, f, indent=4)
            logger.log("Creds", LogLevels.Success, "creds.json saved")
    except Exception as e:
        logger.log("Creds", LogLevels.Error, "Error saving creds")
        logger.log("Creds", LogLevels.Error, e)