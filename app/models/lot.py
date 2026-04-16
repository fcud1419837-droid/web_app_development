import sqlite3
from app.models import get_db


class Lot:
    def __init__(self, id, lot_number, type, poem, explanation, created_at=None):
        self.id = id
        self.lot_number = lot_number
        self.type = type
        self.poem = poem
        self.explanation = explanation
        self.created_at = created_at

    @classmethod
    def _from_row(cls, row):
        """將 sqlite3.Row 轉換成 Lot 物件。"""
        return cls(
            row['id'], row['lot_number'], row['type'],
            row['poem'], row['explanation'], row['created_at']
        )

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    @staticmethod
    def create(lot_number: int, type: str, poem: str, explanation: str):
        """
        新增一首籤詩。

        Args:
            lot_number (int): 籤號（例如 1~100）。
            type (str): 吉凶類型，例如「大吉」、「中吉」、「下下」。
            poem (str): 籤詩內容。
            explanation (str): 解籤說明。

        Returns:
            int: 新籤詩的 id。
        """
        db = get_db()
        try:
            cursor = db.execute(
                "INSERT INTO lots (lot_number, type, poem, explanation) VALUES (?, ?, ?, ?)",
                (lot_number, type, poem, explanation)
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
    def get_by_id(lot_id: int):
        """
        以 id 查詢籤詩。

        Args:
            lot_id (int): 籤詩 id。

        Returns:
            Lot | None: 找到則回傳 Lot 物件，否則回傳 None。
        """
        try:
            db = get_db()
            row = db.execute("SELECT * FROM lots WHERE id = ?", (lot_id,)).fetchone()
            return Lot._from_row(row) if row else None
        except Exception as e:
            raise e

    @staticmethod
    def get_by_lot_number(lot_number: int):
        """
        以籤號查詢籤詩。

        Args:
            lot_number (int): 籤號。

        Returns:
            Lot | None: 找到則回傳 Lot 物件，否則回傳 None。
        """
        try:
            db = get_db()
            row = db.execute(
                "SELECT * FROM lots WHERE lot_number = ?", (lot_number,)
            ).fetchone()
            return Lot._from_row(row) if row else None
        except Exception as e:
            raise e

    @staticmethod
    def get_all():
        """
        取得所有籤詩，依籤號排序。

        Returns:
            list[Lot]: 所有籤詩的列表。
        """
        try:
            db = get_db()
            rows = db.execute("SELECT * FROM lots ORDER BY lot_number ASC").fetchall()
            return [Lot._from_row(r) for r in rows]
        except Exception as e:
            raise e

    @staticmethod
    def get_random():
        """
        隨機抽取一支籤詩。

        Returns:
            Lot | None: 隨機抽到的 Lot 物件，若資料庫無資料回傳 None。
        """
        try:
            db = get_db()
            row = db.execute(
                "SELECT * FROM lots ORDER BY RANDOM() LIMIT 1"
            ).fetchone()
            return Lot._from_row(row) if row else None
        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    @staticmethod
    def update(lot_id: int, lot_number: int, type: str, poem: str, explanation: str):
        """
        更新籤詩內容。

        Args:
            lot_id (int): 籤詩 id。
            lot_number (int): 更新後的籤號。
            type (str): 更新後的吉凶類型。
            poem (str): 更新後的籤詩內容。
            explanation (str): 更新後的解籤說明。
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE lots SET lot_number = ?, type = ?, poem = ?, explanation = ? WHERE id = ?",
                (lot_number, type, poem, explanation, lot_id)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    @staticmethod
    def delete(lot_id: int):
        """
        刪除指定籤詩。

        Args:
            lot_id (int): 籤詩 id。
        """
        db = get_db()
        try:
            db.execute("DELETE FROM lots WHERE id = ?", (lot_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
