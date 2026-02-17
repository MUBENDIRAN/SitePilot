import sqlite3
import json
import requests

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cve(
cve_id TEXT PRIMARY KEY,
published_date TEXT NOT NULL,
last_modified_date TEXT NOT NULL,
description TEXT NOT NULL,
base_score REAL)
"""
)
conn.commit()

def ingest_url(url="https://services.nvd.nist.gov/rest/json/cves/2.0?ResultsPerPage=20"):
    response = requests.get(url)
    data = response.json()

    for item in data.get("vulnerabilities",[]):
        cve = item["cve"]

        cve_id = cve["id"]
        published_date = cve["published"]
        last_modified_date = cve["lastModified"]
        description=""
        for d in cve.get("descriptions",[]):
            if d.get("lang") == "en":
                description = d.get("value")
                break
        base_score = None
        metrics = cve.get("metrics",{})
        if "cvssMetricV2" in metrics:
            base_score = metrics["cvssMetricV2"][0]["cvssData"].get("baseScore")

        cursor.execute("""
        INSERT OR IGNORE INTO cve(
        cve_id,published_date,last_modified_date,description,base_score)
        VALUES (?,?,?,?,?)""",
        (cve_id,published_date,last_modified_date,description,base_score)
        )

    conn.commit()
    conn.close()

def list_cve(cve_id = None,order_by_date=False,page=1,limit=20):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    query = "SELECT * FROM cve "

    param=[]
    if cve_id:
        query+=" WHERE cve_id = ?"
        param.append(cve_id)

    if order_by_date:
        query+=" ORDER BY published_date DESC "

    page = max(page,1)
    limit = min(max(limit,10),100)
    offset = (page - 1)*limit

    query+=" LIMIT ? OFFSET ?"
    param.extend([limit,offset])

    cursor.execute(query,param)
    row = cursor.fetchall()
    conn.close

    return row

if __name__ == "__main__":
    ingest_url()

 

    

