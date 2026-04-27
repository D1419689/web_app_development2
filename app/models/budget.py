import sqlite3
from .db import get_db_connection

class Budget:
    """預算 Model，處理每月預算設定"""

    @staticmethod
    def create(year_month, amount):
        """
        新增一筆預算記錄。
        參數:
            year_month (str): 預算月份 (格式 YYYY-MM)
            amount (float): 預算總額
        回傳:
            int: 新增的預算 ID，若發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO budgets (year_month, amount) VALUES (?, ?)',
                (year_month, amount)
            )
            conn.commit()
            budget_id = cursor.lastrowid
            return budget_id
        except sqlite3.Error as e:
            print(f"Database error in Budget.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有預算記錄。
        回傳:
            list[dict]: 預算清單，失敗則回傳空陣列
        """
        try:
            conn = get_db_connection()
            budgets = conn.execute('SELECT * FROM budgets ORDER BY year_month DESC').fetchall()
            return [dict(row) for row in budgets]
        except sqlite3.Error as e:
            print(f"Database error in Budget.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_year_month(year_month):
        """
        取得特定月份的預算記錄。
        參數:
            year_month (str): 預算月份
        回傳:
            dict: 預算資料，若找不到或發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            budget = conn.execute('SELECT * FROM budgets WHERE year_month = ?', (year_month,)).fetchone()
            return dict(budget) if budget else None
        except sqlite3.Error as e:
            print(f"Database error in Budget.get_by_year_month: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(budget_id, amount):
        """
        更新預算記錄。
        參數:
            budget_id (int): 預算 ID
            amount (float): 新的預算總額
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE budgets SET amount = ? WHERE id = ?',
                (amount, budget_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Budget.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(budget_id):
        """
        刪除預算記錄。
        參數:
            budget_id (int): 預算 ID
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Budget.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
