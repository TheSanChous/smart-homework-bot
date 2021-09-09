from database_context import connection


class GroupInfo:
    def __init__(self,
                 name: str,
                 group_id: int,
                 subjects: list):
        self.name = name
        self.group_id = group_id
        self.subjects = subjects
        pass

    def set_name(self, name):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET name = '{name}' WHERE group_id = {self.group_id}")
        connection.commit()

    def set_subjects(self, subjects: list):
        self.subjects = subjects
