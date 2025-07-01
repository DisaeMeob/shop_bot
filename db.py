import sqlite3

#создание таблицы
def create_table():
  conn = sqlite3.connect('iyoka_db')
  cursor = conn.cursor()
  cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT
)""")
  conn.commit()
  conn.close()
  
#добавление пользователей в бд
def add_user(telegram_id, username):
  conn = sqlite3.connect('iyoka_db')
  cursor = conn.cursor()
  cursor.execute("INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?,?)", (telegram_id, username))
  conn.commit()
  conn.close()

def get_user_id():
  conn = sqlite3.connect('iyoka_db')
  cursor = conn.cursor()
  cursor.execute("SELECT telegram_id FROM users")
  users = cursor.fetchall()
  conn.close()
  return [user_id[0] for user_id in users ]

def get_stat():
  conn = sqlite3.connect('iyoka_db')
  cursor = conn.cursor()
  cursor.execute("SELECT id, username, telegram_id FROM users")
  result = cursor.fetchall()
  conn.close()
  return result



