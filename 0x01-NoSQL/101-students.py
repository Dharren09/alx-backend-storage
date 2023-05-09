#!/usr/bin/env python3

"""function returns all students sorted by average score
the top mut be ordered"""


def top_students(mongo_collection):
    students = mongo_collection.find()
    top_students = []
    for student in students:
        scores = [score.get('score', 0) for score in student.get('topics', [])]
        avg_score = sum(scores) / len(scores) if scores else 0
        student['averageScore'] = avg_score
        top_students.append(student)

    return sorted(top_students, key=lambda s: s.get('averageScore', 0), reverse=True)
