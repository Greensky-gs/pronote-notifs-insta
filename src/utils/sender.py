from typing import List

import pronotepy
from requests import post

from src.cache.data import logger
from src.cache.infos import infos_by_class_name
from src.types.logger import LogLevels


def send_grades(grades_list: List[pronotepy.Grade], url: str):
    def send_chunk(grades: List[pronotepy.Grade]):
        embeds = []

        for grade in grades:
            info = infos_by_class_name.get(grade.subject.name)
            embed = {
                "title": f"Nouvelle note",
                "description": f"**{grade.grade}/{grade.out_of}** en **{grade.subject.name}**",
                "fields": [
                    {
                        "name": "Date",
                        "value": grade.date.strftime("%d/%m/%Y"),
                        "inline": True
                    },
                    {
                        "name": "Coefficient",
                        "value": str(grade.coefficient),
                        "inline": True
                    },
                    {
                        "name": "\u200b",
                        "value": "\u200b",
                        "inline": False
                    },
                    {
                        "name": "Moyenne",
                        "value": f"`{grade.average}/{grade.out_of}`",
                        "inline": True
                    },
                    {
                        "name": "Maximum",
                        "value": f"`{grade.max}/{grade.out_of}`",
                        "inline": True
                    },
                    {
                        "name": "Minimum",
                        "value": f"`{grade.min}/{grade.out_of}`",
                        "inline": True
                    }
                ],
                "timestamp": grade.date.isoformat(),
                "thumbnail": {
                    "url": "https://php-noise.com/noise.php?r=&g=&b=&hex=&tiles=&tileSize=10&borderWidth=&mode=brightness&multi=3&steps=10"
                }
            }

            if info is not None:
                embed["color"] = int(info["color"], 16)
                embed["description"] = f"`{grade.grade}/{grade.out_of}` en **{info['name']}**"

                red, green, blue = int(info["color"][:2], 16), int(info["color"][2:4], 16), int(info["color"][4:], 16)

                embed["thumbnail"]["url"] = f"https://php-noise.com/noise.php?r={red}&g={green}&b={blue}&hex=&tiles=&tileSize=10&borderWidth=&mode=brightness&multi=3&steps=10"
            embeds.append(embed)

        try:
            post(url, json={
                "embeds": embeds
            })
        except Exception as e:
            logger.log("Sender", LogLevels.Error, f"Failed to send chunk")
            logger.log("Sender", LogLevels.Error, e)

    # Chunk the array in 10
    for i in range(0, len(grades_list), 10):
        send_chunk(grades_list[i:i + 10])

def send_new_lesson(lessons_list: List[pronotepy.Lesson], url: str):
    def send_chunk(lessons: List[pronotepy.Lesson]):
        embeds = []

        for lesson in lessons:
            embed = {
                "title": f"Nouveau cours",
                "description": f"**{lesson.subject.name}** avec **{lesson.teacher_name}**",
                "fields": [
                    {
                        "name": "Date",
                        "value": f"`{lesson.start.strftime('%d/%m')}`",
                        "inline": True
                    },
                    {
                        "name": "Début",
                        "value": f'`{lesson.start.strftime("%H:%M")}`',
                        "inline": True
                    },
                    {
                        "name": "Fin",
                        "value": f'`{lesson.end.strftime("%H:%M")}`',
                        "inline": True
                    }
                ],
                "timestamp": lesson.start.isoformat(),
                "thumbnail": {
                    "url": "https://php-noise.com/noise.php?r=&g=&b=&hex=&tiles=&tileSize=10&borderWidth=&mode=brightness&multi=3&steps=10"
                }
            }

            info = infos_by_class_name.get(lesson.subject.name)
            if info is not None:
                embed["color"] = int(info["color"], 16)
                embed["description"] = f"**{info['name']}** avec **{lesson.teacher_name}**"
                embed["thumbnail"]["url"] = f"https://php-noise.com/noise.php?r={int(info['color'][:2], 16)}&g={int(info['color'][2:4], 16)}&b={int(info['color'][4:], 16)}&hex=&tiles=&tileSize=10&borderWidth=&mode=brightness&multi=3&steps=10"


            embeds.append(embed)

        try:
            post(url, json={
                "embeds": embeds
            })
        except Exception as e:
            logger.log("Sender", LogLevels.Error, f"Failed to send chunk")
            logger.log("Sender", LogLevels.Error, e)

    # Chunk the array in 10
    for i in range(0, len(lessons_list), 10):
        send_chunk(lessons_list[i:i + 10])

def send_lessons_updated(lessons_list: List[pronotepy.Lesson], url: str):
    def send_chunk(lessons: List[pronotepy.Lesson]):
        embeds = []

        for lesson in lessons:
            embed = {
                "title": f"Cours mis à jour",
                "description": f"**{lesson.subject.name}** avec **{lesson.teacher_name}**",
                "fields": [
                    {
                        "name": "Date",
                        "value": f"`{lesson.start.strftime('%d/%m')}`",
                        "inline": True
                    },
                    {
                        "name": "Début",
                        "value": f'`{lesson.start.strftime("%H:%M")}`',
                        "inline": True
                    },
                    {
                        "name": "Fin",
                        "value": f'`{lesson.end.strftime("%H:%M")}`',
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": f"`{lesson.status}`",
                        "inline": False
                    }
                ],
                "timestamp": lesson.start.isoformat(),
                "thumbnail": {
                    "url": "https://php-noise.com/noise.php?r=&g=&b=&hex=&tiles=&tileSize=10&borderWidth=&mode=brightness&multi=3&steps=10"
                }
            }

            info = infos_by_class_name.get(lesson.subject.name)
            if info is not None:
                embed["color"] = int(info["color"], 16)
                embed["description"] = f"**{info['name']}** avec **{lesson.teacher_name}**"
                embed["thumbnail"]["url"] = f"https://php-noise.com/noise.php?r={int(info['color'][:2], 16)}&g={int(info['color'][2:4], 16)}&b={int(info['color'][4:], 16)}&hex=&tiles=&tileSize=10&borderWidth=&mode=brightness&multi=3&steps=10"


            embeds.append(embed)

        try:
            post(url, json={
                "embeds": embeds
            })
        except Exception as e:
            logger.log("Sender", LogLevels.Error, f"Failed to send chunk")
            logger.log("Sender", LogLevels.Error, e)

    # Chunk the array in 10
    for i in range(0, len(lessons_list), 10):
        send_chunk(lessons_list[i:i + 10])