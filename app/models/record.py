import sqlite3
from .db import get_db_connection

class Record:
    """收支紀錄 Model，處理日常收入與支出資料"""

    @staticmethod
    def create(type_, amount, category, date, description, account_id):
        """
        新增一筆收支記錄。
        參數:
            type_ (str): 'income' 或 'expense'
            amount (float): 金額
            category (str): 分類
            date (str): 日期 (YYYY-MM-DD)
            description (str): 備註說明
            account_id (int): 關聯的帳戶 ID
        回傳:
            int: 新增的紀錄 ID，失敗則回傳 None
        """
        try:
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
            return record_id
        except sqlite3.Error as e:
            print(f"Database error in Record.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有收支記錄（包含關聯的帳戶名稱）。
        回傳:
            list[dict]: 記錄清單，失敗則回傳空陣列
        """
        try:
            conn = get_db_connection()
            records = conn.execute(
                '''
                SELECT r.*, a.name as account_name 
                FROM records r
                LEFT JOIN accounts a ON r.account_id = a.id
                ORDER BY r.date DESC, r.created_at DESC
                '''
            ).fetchall()
            return [dict(row) for row in records]
        except sqlite3.Error as e:
            print(f"Database error in Record.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(record_id):
        """
        取得單筆收支記錄。
        參數:
            record_id (int): 記錄 ID
        回傳:
            dict: 記錄資料，失敗或找不到則回傳 None
        """
        try:
            conn = get_db_connection()
            record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
            return dict(record) if record else None
        except sqlite3.Error as e:
            print(f"Database error in Record.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(record_id, type_, amount, category, date, description, account_id):
        """
        更新收支記錄。
        參數:
            record_id (int): 記錄 ID
            type_ (str): 'income' 或 'expense'
            amount (float): 金額
            category (str): 分類
            date (str): 日期
            description (str): 備註說明
            account_id (int): 帳戶 ID
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
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
            return True
        except sqlite3.Error as e:
            print(f"Database error in Record.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(record_id):
        """
        刪除收支記錄。
        參數:
            record_id (int): 記錄 ID
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Record.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
