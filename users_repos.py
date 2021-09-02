from database_context import get_connection


class UserInfo:
    def __init__(self, user_id, user_type):
        self.user_id = user_id
        self.type = user_type


def get_user(user_id: int) -> UserInfo:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user is None:
        return None
    user_info = UserInfo(user[2], user[1])
    return user_info


def create_user(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users(type, user_id) VALUES ('user', {user_id})")
    cursor.close()
    connection.commit()
    connection.close()
    pass
