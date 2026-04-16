from app.models import get_db

class Lot:
    def __init__(self, id, lot_number, type, poem, explanation, created_at=None):
        self.id = id
        self.lot_number = lot_number
        self.type = type
        self.poem = poem
        self.explanation = explanation
        self.created_at = created_at

    @staticmethod
    def create(lot_number, type, poem, explanation):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO lots (lot_number, type, poem, explanation) VALUES (?, ?, ?, ?)",
            (lot_number, type, poem, explanation)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(lot_id):
        db = get_db()
        lot = db.execute("SELECT * FROM lots WHERE id = ?", (lot_id,)).fetchone()
        if lot:
            return Lot(lot['id'], lot['lot_number'], lot['type'], lot['poem'], lot['explanation'], lot['created_at'])
        return None

    @staticmethod
    def get_by_lot_number(lot_number):
        db = get_db()
        lot = db.execute("SELECT * FROM lots WHERE lot_number = ?", (lot_number,)).fetchone()
        if lot:
            return Lot(lot['id'], lot['lot_number'], lot['type'], lot['poem'], lot['explanation'], lot['created_at'])
        return None

    @staticmethod
    def get_all():
        db = get_db()
        lots = db.execute("SELECT * FROM lots ORDER BY lot_number ASC").fetchall()
        return [Lot(lot['id'], lot['lot_number'], lot['type'], lot['poem'], lot['explanation'], lot['created_at']) for lot in lots]

    @staticmethod
    def get_random():
        db = get_db()
        lot = db.execute("SELECT * FROM lots ORDER BY RANDOM() LIMIT 1").fetchone()
        if lot:
            return Lot(lot['id'], lot['lot_number'], lot['type'], lot['poem'], lot['explanation'], lot['created_at'])
        return None

    @staticmethod
    def update(lot_id, lot_number, type, poem, explanation):
        db = get_db()
        db.execute(
            "UPDATE lots SET lot_number = ?, type = ?, poem = ?, explanation = ? WHERE id = ?",
            (lot_number, type, poem, explanation, lot_id)
        )
        db.commit()

    @staticmethod
    def delete(lot_id):
        db = get_db()
        db.execute("DELETE FROM lots WHERE id = ?", (lot_id,))
        db.commit()
