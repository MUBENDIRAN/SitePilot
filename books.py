#!/usr/bin/env python3
from fastapi import Body,FastAPI

app = FastAPI()


Books = [ {"title":"title one","year":2000,"author":"author one"},
    {"title":"title oneofone","year":2000,"author":"author one"},
     {"title":"title two","year":2001,"author":"author two"},
      {"title":"title third","year":2002,"author":"author third"},
       {"title":"title four","year":2004,"author":"author four"},
        {"title":"title five","year":2005,"author":"author five"}]


@app.post("/booksadd")
def adding_books(book:dict):
    Books.append(book)


# no need to mention explisit as async since if the function is async fastapi defaultly makes it async
@app.get("/books")
def get_all_books():
    return Books

# we should declare in chronological order because fastapi calls in chronological order
@app.get("/books/mybook")
def test_book():
    return {'my_book':'Linux'}

# dynamic param is used to fetch a unique single value whereas we use explicit fetch for filtering, searching and sorting 
@app.get("/books/{dynamic_param}")
def see_all_books(dynamic_param):
    return {'dynamic_param':dynamic_param}

# the current block should not be after dynamic param if declared it calls the previous dynamic param 
'''
@app.get("/books/mybook")
def test_book():
    return {'my_book':'Linux'}
'''

# this function contains both dynamic and path parameters together and get method should not have body for security concern
@app.get("/Books/{book_year}")
def get_bookk(book_year : int,title : str):
    return_book = []
    for book in Books:
        if book.get('year') == book_year and book.get("title") == title:
            return_book.append(book)
    return return_book



# adding new field of data is post
@app.post("/Books/add_book")
def adding_book(new_book=Body()):
    Books.append(new_book)

# updating new field of data is put
@app.put("/Books/update_book")
def update_book(update_book=Body()):
    for i in range(len(Books)):
        if Books[i].get("year") == update_book.get("year"):
            Books[i] = update_book

# deleting a field of data is delete method
@app.delete("/Books/delete_book/{delete_book}")
def delete_books(delete_book : int):
    for i in range(len(Books)):
        if Books[i].get('year') == delete_book:
            Books.pop(i)
            break

@app.get("/books/assignment/{fetch_all_books}")
def assignment(fetch_all_books : str):
    return_books = []
    for book in Books:
        if book.get('author') == fetch_all_books:
            return_books.append(book)

    return return_books





