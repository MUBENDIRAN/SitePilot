import sqlite3
import json

def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year INTEGER,
        author TEXT
    )
    """)
    conn.commit()
    conn.close()

def load_json_to_db(json_file):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    
    # Clear existing data if any (optional)
    cursor.execute("DELETE FROM books")
    
    with open(json_file, 'r') as f:
        books = json.load(f)
        for book in books:
            cursor.execute(
                "INSERT INTO books (title, year, author) VALUES (?, ?, ?)",
                (book['title'], book['year'], book['author'])
            )
            
    conn.commit()
    conn.close()

def get_books_by_author(author):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    
    # Using manual query
    query = "SELECT title, year, author FROM books WHERE author = ?"
    cursor.execute(query, (author,))
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def get_all_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    
    # Using manual query
    query = "SELECT title, year, author FROM books"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    load_json_to_db("books.json")
    print("Database initialized and data loaded.")
