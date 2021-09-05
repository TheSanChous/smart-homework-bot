from database_context import connection
import random


class GroupInfo:
    def __init__(self,
                 name: str,
                 group_id: int):
        self.name = name
        self.group_id = group_id
        pass

    def set_name(self, name):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET name = '{name}' WHERE group_id = {self.group_id}")
        connection.commit()


def generate_group_id() -> int:
    new_id = int(random.random() * 1000)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM groups WHERE group_id != {new_id}")
    while cursor.fetchone() is not None:
        new_id = random.random() * 1000
        cursor.execute(f"SELECT * FROM groups WHERE group_id != {new_id}")
    return new_id


def create_group(name: str):
    group = GroupInfo(name, generate_group_id())
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO groups(name, group_id) VALUES ({group.name}, {group.group_id})")
    connection.commit()
    return group


def get_group(group_id: int) -> GroupInfo:
    cursor = connection.cursor()
    cursor.execute(f"SELECT name, group_id FROM groups WHERE group_id = {group_id}")
    result = cursor.fetchone()
    if result is None:
        return None
    group = GroupInfo(name=result[0], group_id=result[1])
    return group


def get_group_by_name(group_name: str) -> GroupInfo:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM groups WHERE group_id = {group_name}")
    result = cursor.fetchone()
    if result is None:
        return None
    group = GroupInfo(result[0], result[1])
    return group
