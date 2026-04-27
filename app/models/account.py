import sqlite3
from .db import get_db_connection

class Account:
    """帳戶 Model，處理現金、信用卡等資金來源"""

    @staticmethod
    def create(name, initial_balance=0.0):
        """
        新增一筆帳戶記錄。
        參數:
            name (str): 帳戶名稱
            initial_balance (float): 初始餘額
        回傳:
            int: 新增的帳戶 ID，若發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO accounts (name, initial_balance) VALUES (?, ?)',
                (name, initial_balance)
            )
            conn.commit()
            account_id = cursor.lastrowid
            return account_id
        except sqlite3.Error as e:
            print(f"Database error in Account.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有帳戶記錄。
        回傳:
            list[dict]: 帳戶清單，若發生錯誤則回傳空陣列
        """
        try:
            conn = get_db_connection()
            accounts = conn.execute('SELECT * FROM accounts ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in accounts]
        except sqlite3.Error as e:
            print(f"Database error in Account.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(account_id):
        """
        取得單筆帳戶記錄。
        參數:
            account_id (int): 帳戶 ID
        回傳:
            dict: 帳戶資料，若找不到或發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            account = conn.execute('SELECT * FROM accounts WHERE id = ?', (account_id,)).fetchone()
            return dict(account) if account else None
        except sqlite3.Error as e:
            print(f"Database error in Account.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(account_id, name, initial_balance):
        """
        更新帳戶記錄。
        參數:
            account_id (int): 帳戶 ID
            name (str): 新名稱
            initial_balance (float): 新餘額
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE accounts SET name = ?, initial_balance = ? WHERE id = ?',
                (name, initial_balance, account_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Account.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(account_id):
        """
        刪除帳戶記錄。
        參數:
            account_id (int): 帳戶 ID
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Account.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
