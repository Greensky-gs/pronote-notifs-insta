import datetime
from os import getenv
from typing import List

import pronotepy

from src.cache.data import logger, lessons_database
from src.types.lessons import StoredClass
from src.types.logger import LogLevels
from src.utils.obfuscators import identify_lesson
from src.utils.sender import send_new_lesson, send_lessons_updated


def run_lessons(client: pronotepy.Client):
    logger.log("Lessons", LogLevels.Info, "Fetching lessons")

    now = datetime.datetime.now()
    this_morning = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)

    stored_lessons = lessons_database.data

    def check_at(date: datetime.datetime):
        logger.log("Lessons", LogLevels.Debug, f"Checking lessons at {date.strftime('%d/%m')}")
        lessons = client.lessons(date)

        new_lessons_Lesson: List[pronotepy.Lesson] = []
        new_lessons_Stored: List[StoredClass] = []

        lessons_to_update_Lesson: List[pronotepy.Lesson] = []
        lessons_to_update: List[StoredClass] = []

        lessons_database.bulk()

        for lesson in lessons:
            lesson_id = identify_lesson(lesson)

            found_in_db = any(map(lambda x: x["id"] == lesson_id, stored_lessons))

            if not found_in_db:
                logger.log("Lessons", LogLevels.Debug, f"New lesson found: {lesson_id}")

                new_lessons_Lesson.append(lesson)
                new_lessons_Stored.append({
                    "id": lesson_id,
                    "subject": lesson.subject.name,
                    "status": lesson.status,
                    "num": lesson.num
                })
            else:
                stored_lesson = list(filter(lambda x: x["id"] == lesson_id, stored_lessons))[0]

                if stored_lesson["status"] != lesson.status:
                    logger.log("Lessons", LogLevels.Debug, f"Lesson status changed: {lesson_id}")

                    lessons_to_update_Lesson.append(lesson)
                    lessons_to_update.append({
                        "id": lesson_id,
                        "subject": lesson.subject.name,
                        "status": lesson.status,
                        "num": lesson.num
                    })

        lessons_database.append_datas(new_lessons_Stored)

        for lesson_to_up in lessons_to_update:
            element_of_db = list(filter(lambda x: x["id"] == lesson_to_up["id"] , stored_lessons))[0]

            lessons_database.remove_data(element_of_db)
            lessons_database.append_data(lesson_to_up)

        # Apply a filter to remove duplicated lessons (by id)
        def filter_new_datas():
            stored: List[str] = []

            for x in lessons_database.data:
                if x["id"] not in stored:
                    stored.append(x["id"])
                else:
                    lessons_database.remove_data(x)
        filter_new_datas()

        lessons_database.unbulk()

        if len(new_lessons_Lesson) > 0:
            logger.log("Lessons", LogLevels.Info, f"Sending {len(new_lessons_Lesson)} new lessons")
            send_new_lesson(new_lessons_Lesson, getenv('discord_webhook_lessons'))

        if len(lessons_to_update_Lesson) > 0:
            logger.log("Lessons", LogLevels.Info, f"Sending {len(lessons_to_update_Lesson)} updated lessons")
            send_lessons_updated(lessons_to_update_Lesson, getenv('discord_webhook_lessons'))

    check_at(this_morning)