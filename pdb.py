import sqlite3
def create_photo_db():
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS photos(category TEXT, product_code TEXT UNIQUE, file_id TEXT)')
    conn.commit()
    conn.close()
def exist(product_code):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM photos WHERE product_code = ?',(product_code,))
    result = cursor.fetchone()
    conn.close()
    return result
    
def add_photo(category,product_code, file_id):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO photos(category,product_code,file_id) VALUES(?,?,?)',(category,product_code,file_id))
    conn.commit()
    conn.close()

def get_photo(category,product_code):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_id FROM photos WHERE category = ? AND product_code = ?', (category,product_code))
    result = cursor.fetchone()
    conn.close()
    return result