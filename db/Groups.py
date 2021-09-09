from database_context import connection


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
