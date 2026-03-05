from fastapi import FastAPI, HTTPException
from books_db import get_all_books, get_books_by_author, init_db, load_json_to_db

app = FastAPI()

# Initialize and load data on startup (simple way for this exercise)
@app.on_event("startup")
def startup_event():
    init_db()
    load_json_to_db("books.json")

@app.get("/books")
def fetch_all_books():
    books_data = get_all_books()
    result = []
    for item in books_data:
        result.append({
            "title": item[0],
            "year": item[1],
            "author": item[2]
        })
    return {"data": result}

@app.get("/books/{author}")
def fetch_books_by_author(author: str):
    books_data = get_books_by_author(author)
    if not books_data:
        raise HTTPException(status_code=404, detail="No books found for this author")
    
    result = []
    for item in books_data:
        result.append({
            "title": item[0],
            "year": item[1],
            "author": item[2]
        })
    return {"author": author, "data": result}
