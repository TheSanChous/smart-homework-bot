from db.database_context import connection
from datetime import datetime


class HomeworkInfo:
    def __init__(self,
                 homework_id: int,
                 subject_id: int,
                 description: str,
                 date: datetime):
        self.homework_id = homework_id
        self.subject_id = subject_id
        self.description = description
        self.date = date
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

    def set_date(self, date: datetime):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE homeworks SET date = '{date.year}-{date.month}-{date.day}'")
        connection.commit()
        self.date = date

    def delete(self):
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM homeworks WHERE id = {self.homework_id}")
        pass
