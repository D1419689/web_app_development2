from .db import get_db_connection

class Record:
    @staticmethod
    def create(type_, amount, category, date, description, account_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO records (type, amount, category, date, description, account_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (type_, amount, category, date, description, account_id)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        records = conn.execute(
            '''
            SELECT r.*, a.name as account_name 
            FROM records r
            LEFT JOIN accounts a ON r.account_id = a.id
            ORDER BY r.date DESC, r.created_at DESC
            '''
        ).fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def update(record_id, type_, amount, category, date, description, account_id):
        conn = get_db_connection()
        conn.execute(
            '''
            UPDATE records 
            SET type = ?, amount = ?, category = ?, date = ?, description = ?, account_id = ?
            WHERE id = ?
            ''',
            (type_, amount, category, date, description, account_id, record_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
