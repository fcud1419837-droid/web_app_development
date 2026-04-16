import sqlite3
from app.models import get_db


class Record:
    def __init__(self, id, user_id, lot_id, created_at=None, lot=None):
        self.id = id
        self.user_id = user_id
        self.lot_id = lot_id
        self.created_at = created_at
        self.lot = lot  # 選擇性附加的 Lot 物件（JOIN 查詢時使用）

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    @staticmethod
    def create(user_id: int, lot_id: int):
        """
        新增一筆抽籤歷史紀錄。

        Args:
            user_id (int): 抽籤的使用者 id。
            lot_id (int): 抽到的籤詩 id。

        Returns:
            int: 新紀錄的 id。
        """
        db = get_db()
        try:
            cursor = db.execute(
                "INSERT INTO records (user_id, lot_id) VALUES (?, ?)",
                (user_id, lot_id)
            )
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            db.rollback()
            raise e

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    @staticmethod
    def get_by_id(record_id: int):
        """
        以 id 查詢一筆抽籤紀錄，並 JOIN 取得籤詩詳情。

        Args:
            record_id (int): 紀錄 id。

        Returns:
            Record | None: 找到則回傳帶有 lot 屬性的 Record 物件，否則回傳 None。
        """
        try:
            db = get_db()
            query = """
                SELECT r.id, r.user_id, r.lot_id, r.created_at,
                       l.lot_number, l.type, l.poem, l.explanation
                FROM records r
                LEFT JOIN lots l ON r.lot_id = l.id
                WHERE r.id = ?
            """
            row = db.execute(query, (record_id,)).fetchone()
            if not row:
                return None
            return Record._build(row)
        except Exception as e:
            raise e

    @staticmethod
    def get_by_user_id(user_id: int):
        """
        取得指定使用者的所有抽籤紀錄，包含籤詩詳情，依時間倒序排列。

        Args:
            user_id (int): 使用者 id。

        Returns:
            list[Record]: 該使用者所有抽籤紀錄的列表。
        """
        try:
            db = get_db()
            query = """
                SELECT r.id, r.user_id, r.lot_id, r.created_at,
                       l.lot_number, l.type, l.poem, l.explanation
                FROM records r
                LEFT JOIN lots l ON r.lot_id = l.id
                WHERE r.user_id = ?
                ORDER BY r.created_at DESC
            """
            rows = db.execute(query, (user_id,)).fetchall()
            return [Record._build(row) for row in rows]
        except Exception as e:
            raise e

    @staticmethod
    def get_all():
        """
        取得所有抽籤紀錄（不含籤詩詳情）。

        Returns:
            list[Record]: 所有抽籤紀錄列表。
        """
        try:
            db = get_db()
            rows = db.execute(
                "SELECT * FROM records ORDER BY created_at DESC"
            ).fetchall()
            return [Record(r['id'], r['user_id'], r['lot_id'], r['created_at']) for r in rows]
        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    @staticmethod
    def delete(record_id: int):
        """
        刪除指定的抽籤紀錄。

        Args:
            record_id (int): 紀錄 id。
        """
        db = get_db()
        try:
            db.execute("DELETE FROM records WHERE id = ?", (record_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    # ------------------------------------------------------------------
    # 私有輔助方法
    # ------------------------------------------------------------------
    @staticmethod
    def _build(row):
        """將含有 JOIN 籤詩欄位的 sqlite3.Row 轉換成 Record 物件（含 lot 屬性）。"""
        from .lot import Lot
        lot = None
        if row['lot_number'] is not None:
            lot = Lot(
                id=row['lot_id'],
                lot_number=row['lot_number'],
                type=row['type'],
                poem=row['poem'],
                explanation=row['explanation']
            )
        return Record(row['id'], row['user_id'], row['lot_id'], row['created_at'], lot=lot)
