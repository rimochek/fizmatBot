import sqlite3 as sqlite
import logging

class DatabaseManager(object):
    def __init__(self, path):
        self.connect = sqlite.connect(path)
        self.connect.execute("pragma foreign_keys = on")
        self.connect.commit()
        self.cur = self.connect.cursor()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER UNIQUE,
            name TEXT,
            language TEXT,
            date TEXT
        );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS messages(
            id INTEGER,
            name TEXT,
            context TEXT,
            date TEXT
        );''')
    
    def add_user(self, message):
        values = [message.chat.id, message.from_user.username, "kz", message.date]
        try:
            self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", values)
            self.connect.commit()
            logging.info(f"User: {values[0]}, добавлен в базу данных")
            return True
        except:
            logging.info(f"User: {values[0]}, не может быть добавлен в БД, так как он уже там находится")
            return False

    def add_message(self, message):
        values = [message.chat.id, message.from_user.username, message.text, message.date]
        self.cur.execute("INSERT INTO messages VALUES(?, ?, ?, ?)", values)
        self.connect.commit()
    
    def get_user_language(self, id):
        self.cur.execute(f"SELECT language FROM users WHERE id = {id}")
        language = self.cur.fetchone()[0]

        if language == 'kz' or language == 'ru':
            return language
        else:
            return 'kz'
    
    def set_user_language(self, id, language):
        self.cur.execute(f"UPDATE users SET language = ? WHERE id = ?", (language, id))
        self.connect.commit()
        logging.info(f"User: {id}, поменял язык на {language}")

    def __del__(self):
        self.connect.close()