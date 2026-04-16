import sqlite3
import bcrypt
from app.models import get_db


class User:
    def __init__(self, id, username, password_hash, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    @staticmethod
    def create(username: str, password: str):
        """
        建立新使用者，密碼會以 bcrypt 加密後儲存。

        Args:
            username (str): 唯一帳號名稱。
            password (str): 明文密碼。

        Returns:
            int | None: 新使用者的 id，若帳號已存在則回傳 None。
        """
        db = get_db()
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        try:
            cursor = db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # 帳號已存在（username UNIQUE 約束）
            return None
        except Exception as e:
            db.rollback()
            raise e

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    @staticmethod
    def get_by_id(user_id: int):
        """
        以 id 查詢使用者。

        Args:
            user_id (int): 使用者 id。

        Returns:
            User | None: 找到則回傳 User 物件，否則回傳 None。
        """
        try:
            db = get_db()
            row = db.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row:
                return User(row['id'], row['username'], row['password_hash'], row['created_at'])
            return None
        except Exception as e:
            raise e

    @staticmethod
    def get_by_username(username: str):
        """
        以帳號名稱查詢使用者。

        Args:
            username (str): 帳號名稱。

        Returns:
            User | None: 找到則回傳 User 物件，否則回傳 None。
        """
        try:
            db = get_db()
            row = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
            if row:
                return User(row['id'], row['username'], row['password_hash'], row['created_at'])
            return None
        except Exception as e:
            raise e

    @staticmethod
    def get_all():
        """
        取得所有使用者。

        Returns:
            list[User]: 所有使用者的列表。
        """
        try:
            db = get_db()
            rows = db.execute(
                "SELECT * FROM users ORDER BY created_at DESC"
            ).fetchall()
            return [User(r['id'], r['username'], r['password_hash'], r['created_at']) for r in rows]
        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    @staticmethod
    def update_password(user_id: int, new_password: str):
        """
        更新使用者密碼（自動重新加密）。

        Args:
            user_id (int): 使用者 id。
            new_password (str): 新的明文密碼。
        """
        db = get_db()
        new_hash = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        try:
            db.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_hash, user_id)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    @staticmethod
    def delete(user_id: int):
        """
        刪除指定使用者（相關的 records 會因 CASCADE 一起被刪除）。

        Args:
            user_id (int): 使用者 id。
        """
        db = get_db()
        try:
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    # ------------------------------------------------------------------
    # 驗證密碼
    # ------------------------------------------------------------------
    def check_password(self, password: str) -> bool:
        """
        驗證輸入的密碼是否與儲存的 hash 相符。

        Args:
            password (str): 使用者輸入的明文密碼。

        Returns:
            bool: 相符回傳 True，否則回傳 False。
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
