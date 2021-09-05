from database_context import connection
from group_repos import GroupInfo
user_types = [
    "teacher",
    "student"
]


class UserInfo:
    def __init__(self,
                 user_id: int,
                 user_type: str,
                 is_registered: bool,
                 first_name: str,
                 last_name: str,
                 state: str,
                 group_id: int):
        self.user_id = user_id
        self.type = user_type
        self.is_registered = is_registered
        self.first_name = first_name
        self.last_name = last_name
        self.state = state
        self.group_id = group_id
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

    def set_group(self, group: GroupInfo):
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET group_id = '{group.group_id}' WHERE user_id = {self.user_id}")
        connection.commit()
        self.group_id = group.group_id
        pass


def get_user(user_id: int) -> UserInfo:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        return create_user(user_id)
    user_info = UserInfo(user[2], user[1], user[3], user[4], user[5], user[6], user[7])
    return user_info


def create_user(user_id: int) -> UserInfo:
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users(type, user_id) VALUES ('user', {user_id})")
    connection.commit()
    cursor.close()
    return get_user(user_id)
