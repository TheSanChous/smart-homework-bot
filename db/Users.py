from database_context import connection
from db import Groups, Subjects


class UserInfo:
    def __init__(self,
                 user_id: int,
                 user_type: str,
                 is_registered: bool,
                 first_name: str,
                 last_name: str,
                 state: str,
                 groups: list,
                 selected_group: Groups.GroupInfo,
                 selected_subject: Subjects.SubjectInfo):
        self.user_id = user_id
        self.type = user_type
        self.is_registered = is_registered
        self.first_name = first_name
        self.last_name = last_name
        self.state = state
        self.groups = groups
        self.selected_group = selected_group
        self.selected_subject = selected_subject
        pass

    def set_type(self, user_type: str):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET type = '{user_type}' WHERE user_id = {self.user_id}")
        connection.commit()
        self.type = user_type
        pass

    def set_registered(self, is_registered: bool):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET is_registered = {is_registered} WHERE user_id = {self.user_id}")
        connection.commit()
        self.is_registered = is_registered
        pass

    def set_first_name(self, first_name: str):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET first_name = '{first_name}' WHERE user_id = {self.user_id}")
        connection.commit()
        self.first_name = first_name
        pass

    def set_last_name(self, last_name: str):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET last_name = '{last_name}' WHERE user_id = {self.user_id}")
        connection.commit()
        self.last_name = last_name
        pass

    def set_state(self, state: str):
        cursor = connection.cursor()
        self.state = state
        if state is None:
            state = 'null'
        else:
            state = f"'{state}'"
        cursor.execute(f"UPDATE users SET state = {state} WHERE user_id = {self.user_id}")
        connection.commit()
        pass

    def add_group(self, group: Groups.GroupInfo):
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO users_groups(user_id, group_id) VALUES('{self.user_id}', {group.group_id})")
        connection.commit()
        self.groups.append(group)
        pass

    def set_selected_group(self, group: Groups.GroupInfo):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET selected_group_id = {group.group_id if group is not None else 'NULL'} WHERE user_id = {self.user_id}")
        connection.commit()
        self.selected_group = group
        pass

    def set_selected_subject(self, subject: Subjects.SubjectInfo):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET selected_subject_id = {subject.subject_id if subject is not None else 'NULL'} WHERE user_id = {self.user_id}")
        connection.commit()
        self.selected_subject = subject
