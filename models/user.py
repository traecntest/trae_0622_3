from .database import Database


class User:
    def __init__(self, id=None, username=None, nickname=None, age=None,
                 is_elderly_mode=False, created_at=None):
        self.id = id
        self.username = username
        self.nickname = nickname
        self.age = age
        self.is_elderly_mode = is_elderly_mode
        self.created_at = created_at

    @staticmethod
    def create(username, nickname=None, age=None, is_elderly_mode=False):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, nickname, age, is_elderly_mode) VALUES (?, ?, ?, ?)",
            (username, nickname, age, 1 if is_elderly_mode else 0)
        )
        conn.commit()
        return User.get_by_id(cursor.lastrowid)

    @staticmethod
    def get_by_id(user_id):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                username=row["username"],
                nickname=row["nickname"],
                age=row["age"],
                is_elderly_mode=bool(row["is_elderly_mode"]),
                created_at=row["created_at"]
            )
        return None

    @staticmethod
    def get_by_username(username):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                username=row["username"],
                nickname=row["nickname"],
                age=row["age"],
                is_elderly_mode=bool(row["is_elderly_mode"]),
                created_at=row["created_at"]
            )
        return None

    def update(self):
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username=?, nickname=?, age=?, is_elderly_mode=? WHERE id=?",
            (self.username, self.nickname, self.age,
             1 if self.is_elderly_mode else 0, self.id)
        )
        conn.commit()

    @staticmethod
    def list_all():
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [User(
            id=row["id"],
            username=row["username"],
            nickname=row["nickname"],
            age=row["age"],
            is_elderly_mode=bool(row["is_elderly_mode"]),
            created_at=row["created_at"]
        ) for row in rows]
