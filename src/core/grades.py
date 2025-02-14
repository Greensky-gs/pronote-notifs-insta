from os import getenv
from typing import List

import pronotepy

from src.cache.data import logger, grades_database
from src.classes.Logger import Logger
from src.types.logger import LogLevels, ColorCodes
from src.utils.obfuscators import identify_grade
from src.utils.sender import send_grades


def run_grades(client: pronotepy.Client):
    logger.log("Grades", LogLevels.Info, "Fetching grades")

    elements = grades_database.data
    unknown: List[pronotepy.Grade] = []

    for grade in client.current_period.grades:
        grade_id = identify_grade(grade)

        if not grade_id in elements:
            unknown.append(grade)

    logger.log("Grades", LogLevels.Debug, f"Found {Logger.chalk(ColorCodes.Red, str(len(unknown)))} new grades")
    grades_database.append_datas(list(map(lambda x: identify_grade(x), unknown)))

    logger.log('Grades', LogLevels.Info, f"Sending {Logger.chalk(ColorCodes.Red, str(len(unknown)))} new grades")
    send_grades(unknown, getenv("discord_webhook"))
