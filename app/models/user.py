from app.models import get_db

class User:
    def __init__(self, id, username, password_hash, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    @staticmethod
    def create(username, password_hash):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            db.commit()
            return cursor.lastrowid
        except db.IntegrityError:
            return None  # Username already exists

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            return User(user['id'], user['username'], user['password_hash'], user['created_at'])
        return None

    @staticmethod
    def get_by_username(username):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            return User(user['id'], user['username'], user['password_hash'], user['created_at'])
        return None

    @staticmethod
    def update_password(user_id, new_password_hash):
        db = get_db()
        db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, user_id)
        )
        db.commit()

    @staticmethod
    def delete(user_id):
        db = get_db()
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
