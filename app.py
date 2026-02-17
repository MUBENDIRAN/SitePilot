from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import list_cve
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credential=True,
    allow_header="*",
    allow_methods="*"
)

@app.get("/list_cve")
def list_of_cve(
    cve_id:Optional[str] = None,
    order_by_date:bool = False,
    page: int = Query (1,ge=1),
    limit: int = Query(20,le=100)):

    result = []
    try:
        list_cve_of = list_cve(cve_id,order_by_date,page,limit)
    except Exception:
        raise HTTPException(status_code=500,detail="Internal Server Error")
    for item in list_cve_of:
        result.append({
            "cve_id":item[0],
            "published_date":item[1],
            "last_modified_date":item[2],
            "description":item[3],
            "base_score":item[4]
        }
        )

    return {
        "count":len(result),
        "page":page,
        "limit":limit,
        "data":result
    }