from .db import get_db_connection

class Budget:
    @staticmethod
    def create(year_month, amount):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO budgets (year_month, amount) VALUES (?, ?)',
            (year_month, amount)
        )
        conn.commit()
        budget_id = cursor.lastrowid
        conn.close()
        return budget_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        budgets = conn.execute('SELECT * FROM budgets ORDER BY year_month DESC').fetchall()
        conn.close()
        return [dict(row) for row in budgets]

    @staticmethod
    def get_by_year_month(year_month):
        conn = get_db_connection()
        budget = conn.execute('SELECT * FROM budgets WHERE year_month = ?', (year_month,)).fetchone()
        conn.close()
        return dict(budget) if budget else None

    @staticmethod
    def update(budget_id, amount):
        conn = get_db_connection()
        conn.execute(
            'UPDATE budgets SET amount = ? WHERE id = ?',
            (amount, budget_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(budget_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
        conn.commit()
        conn.close()
