#!/usr/bin/env python3
from fastapi import FastAPI

app = FastAPI()


Books = [
    {"title":"title one","year":2000,"author":"author one"},
     {"title":"title two","year":2001,"author":"author two"},
      {"title":"title third","year":2002,"author":"author third"},
       {"title":"title four","year":2004,"author":"author four"},
        {"title":"title five","year":2005,"author":"author five"}
]


# no need to mention explisit as async since if the function is async fastapi defaultly makes it async
@app.get("/books")
def get_all_books():
    return Books
