import sqlite3

class BaseData:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def sqlite(self, sql : str):
        with self.connection:
            return self.cursor.execute(sql).fetchall()
    def sqlite1(self, sql : str, params):
        with self.connection:
            return self.cursor.execute(sql, params).fetchall()


    def insert_user_data(self, fullname : str, username : str, answer : str, user_id : int):
        with self.connection:
            self.cursor.execute('INSERT INTO Users VALUES (?, ?, ?, ?)', (fullname, username, answer, user_id))
    def get_user_info(self, user_id : int, data : str = '*'):
        with self.connection:
            return self.cursor.execute(f"SELECT {data} FROM Users WHERE user_id = {user_id}").fetchone()

    def get_receivers_list(self, letters : str = ''):
        with self.connection:
            return self.cursor.execute(f"SELECT user_id, fullname FROM Users WHERE user_id LIKE '{letters}%' LIMIT 24").fetchall()   
    
    @property
    def get_num(self):
        with self.connection:
            self.cursor.execute(f"UPDATE Info SET num = num + 1")
            return self.cursor.execute(f"SELECT num FROM Info").fetchone()[0]
    
    def get_text(self, key : str):
        with self.connection:
            return self.cursor.execute(f"SELECT Text1 FROM Texts WHERE key = '{key}'").fetchone()[0]

    def get_questions(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM Questions').fetchall()