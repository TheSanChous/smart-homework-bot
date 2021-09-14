from db.database_context import connection


class HomeworkInfo:
    def __init__(self,
                 homework_id: int,
                 subject_id: int,
                 description: str):
        self.homework_id = homework_id
        self.subject_id = subject_id
        self.description = description
        pass

    def set_subject_id(self, subject_id):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE homeworks SET subject_id = '{subject_id}' WHERE id = {self.homework_id}")
        connection.commit()
        self.subject_id = subject_id
        pass

    def set_description(self, description):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE homeworks SET description = '{description if description is not None else 'NULL'}'" +
                       f" WHERE id = {self.homework_id}")
        connection.commit()
        self.description = description
        pass

    def delete(self):
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM homeworks WHERE id = {self.homework_id}")
        pass
