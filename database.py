import sqlite3
import random
import string
class Database:
    def __init__(self, db_path="life_fitness.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # nicer dict-like rows
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS overdue ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                amount REAL, 
                phone TEXT, 
                email TEXT 
            )
        """)
        self.seed_overdue_data(100) # seed with 100 records
    def query(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def execute(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()

    def seed_overdue_data(self,recordNum): 

        # Check if table already has data 
        count = self.query("SELECT COUNT(*) AS c FROM overdue")[0]["c"] 
        if count > 0: return # already seeded 

        for i in range(1, recordNum+1): 
            if i == 1:
                name = "Stevie Watts" 
                amount = 250.75
                phone = "07123456789"
                email = "Stevie.Watts.655@cranfield.ac.uk"
            else :
                name = f"test{i}" 
                amount = round(random.uniform(1, 1000), 2)
                phone ="07" + "".join(random.choices(string.digits, k=9))
                email = "test" + str(i) + "@example.com"
            self.execute( 
                "INSERT INTO overdue (name, amount, phone, email) VALUES (?, ?, ?, ?)",
                (name, amount, phone, email) ) 
            
    def close(self):
        self.conn.close()
