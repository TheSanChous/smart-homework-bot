from db.database_context import connection


class SubjectInfo:
    def __init__(self,
                 subject_id: int,
                 name: str,
                 description: str,
                 group_id: int):
        self.subject_id = subject_id
        self.name = name
        self.description = description
        self.group_id = group_id
        pass

    def set_name(self, name: str):
        cursor = connection.cursor()
        cursor.execute(F"UPDATE subjects SET name = '{name}' WHERE id = {self.subject_id}")
        connection.commit()
        self.name = name
        pass

    def set_description(self, description: str):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE subjects SET description = '{description}' WHERE id = {self.subject_id}")
        connection.commit()
        self.description = description
        pass
