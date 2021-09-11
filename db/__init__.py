from . import Subjects
from . import Users
from . import Groups
from . import Homeworks
from database_context import connection
import random


def get_groups(user_id: int) -> list:
    cursor = connection.cursor()
    cursor.execute(f"SELECT group_id FROM users_groups WHERE user_id = {user_id}")
    results = cursor.fetchall()
    groups = list()
    for result in results:
        group = get_group(result[0])
        groups.append(group)
    cursor.close()
    return groups


def get_subjects(group_id: int):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM subjects WHERE group_id = {group_id}")
    results = cursor.fetchall()
    subjects = []
    for result in results:
        subjects.append(Subjects.SubjectInfo(result[0], result[1], result[2], result[3]))
    return subjects


def get_user(user_id: int) -> Users.UserInfo:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        return create_user(user_id)
    user_info = Users.UserInfo(user[2], user[1], user[3], user[4], user[5], user[6], get_groups(user[2]), get_group(user[7]), get_subject(user[8]), get_homework(user[9]))
    return user_info


def create_user(user_id: int) -> Users.UserInfo:
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users(type, user_id) VALUES ('user', {user_id})")
    connection.commit()
    cursor.close()
    return get_user(user_id)


def create_subject(name: str, group: Groups.GroupInfo):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO subjects(name, group_id) VALUES('{name}', {group.group_id});" +
                   "SELECT MAX(id) as id FROM subjects LIMIT 1;")
    subject_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return Subjects.SubjectInfo(subject_id=subject_id, name=name, description="", group_id=group.group_id)


def get_subject(subject_id: int):
    if subject_id is None:
        return None
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, name, description, group_id FROM subjects WHERE id = {subject_id}")
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    subject = Subjects.SubjectInfo(subject_id=result[0], name=result[1], description=result[2], group_id=result[3])
    return subject


def generate_group_id() -> int:
    new_id = 1000 + int(random.random() * 9999)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM groups WHERE group_id = {new_id}")
    if cursor.fetchone() is not None:
        return generate_group_id()
    return new_id


def create_group(name: str):
    group_id = generate_group_id()
    group = Groups.GroupInfo(name, group_id, get_subjects(group_id))
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO groups(name, group_id) VALUES ('{group.name}', {group.group_id})")
    connection.commit()
    cursor.close()
    return group


def get_group(group_id: int) -> Groups.GroupInfo:
    if group_id is None:
        return None
    cursor = connection.cursor()
    cursor.execute(f"SELECT name, group_id FROM groups WHERE group_id = {group_id}")
    result = cursor.fetchone()
    if result is None:
        return None
    group = Groups.GroupInfo(name=result[0], group_id=result[1], subjects=get_subjects(group_id))
    return group


def get_group_by_name(group_name: str) -> Groups.GroupInfo:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM groups WHERE group_id = {group_name}")
    result = cursor.fetchone()
    if result is None:
        return None
    group = Groups.GroupInfo(result[0], result[1], get_subjects(result[1]))
    return group


def create_homework(subject: Subjects.SubjectInfo, description: str):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO homeworks(subject_id, description) VALUES ({subject.subject_id}, '{description}');"
                   "SELECT MAX(id) as id FROM homeworks LIMIT 1;")
    homework_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return Homeworks.HomeworkInfo(homework_id=homework_id, subject_id=subject.subject_id, description=description)


def get_homework(homework_id: int) -> Homeworks.HomeworkInfo:
    if homework_id is None:
        return None
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM homeworks WHERE id = {homework_id}")
    result = cursor.fetchone()
    if result is None:
        return None
    homework = Homeworks.HomeworkInfo(homework_id=result[0], subject_id=result[1], description=result[2])
    return homework
