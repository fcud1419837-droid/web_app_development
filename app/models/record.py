from app.models import get_db

class Record:
    def __init__(self, id, user_id, lot_id, created_at=None, lot=None):
        self.id = id
        self.user_id = user_id
        self.lot_id = lot_id
        self.created_at = created_at
        self.lot = lot  # Optional Lot object for convenience

    @staticmethod
    def create(user_id, lot_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO records (user_id, lot_id) VALUES (?, ?)",
            (user_id, lot_id)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(record_id):
        db = get_db()
        # Join with lots to get the lot details if needed
        query = """
            SELECT r.*, l.lot_number, l.type, l.poem, l.explanation 
            FROM records r 
            LEFT JOIN lots l ON r.lot_id = l.id 
            WHERE r.id = ?
        """
        row = db.execute(query, (record_id,)).fetchone()
        
        if row:
            # We can optionally instantiate a Lot object here if needed
            from .lot import Lot
            lot = None
            if row['lot_number'] is not None:
                lot = Lot(row['lot_id'], row['lot_number'], row['type'], row['poem'], row['explanation'])
                
            return Record(row['id'], row['user_id'], row['lot_id'], row['created_at'], lot=lot)
        return None

    @staticmethod
    def get_by_user_id(user_id):
        db = get_db()
        query = """
            SELECT r.*, l.lot_number, l.type, l.poem, l.explanation 
            FROM records r 
            LEFT JOIN lots l ON r.lot_id = l.id 
            WHERE r.user_id = ?
            ORDER BY r.created_at DESC
        """
        rows = db.execute(query, (user_id,)).fetchall()
        records = []
        from .lot import Lot
        for row in rows:
            lot = None
            if row['lot_number'] is not None:
                lot = Lot(row['lot_id'], row['lot_number'], row['type'], row['poem'], row['explanation'])
            records.append(Record(row['id'], row['user_id'], row['lot_id'], row['created_at'], lot=lot))
        return records

    @staticmethod
    def get_all():
        db = get_db()
        rows = db.execute("SELECT * FROM records ORDER BY created_at DESC").fetchall()
        return [Record(row['id'], row['user_id'], row['lot_id'], row['created_at']) for row in rows]

    @staticmethod
    def delete(record_id):
        db = get_db()
        db.execute("DELETE FROM records WHERE id = ?", (record_id,))
        db.commit()
