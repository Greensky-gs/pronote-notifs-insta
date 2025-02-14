import hashlib
import pronotepy


def hash_string(input_string: str) -> str:
    hash_object = hashlib.sha256()

    hash_object.update(input_string.encode('utf-8'))

    hex_dig = hash_object.hexdigest()

    return hex_dig

def identify_grade(grade: pronotepy.Grade):
    return hash_string(grade.subject.name + grade.date.strftime("%d/%m/%Y") + grade.period.name)

def identify_lesson(lesson: pronotepy.Lesson):
    return hash_string(lesson.subject.name + lesson.background_color + lesson.teacher_name + lesson.start.strftime("%d/%m/%Y %H:%M") + lesson.end.strftime("%d/%m/%Y %H:%M") + lesson.status if lesson.status is not None else "")