# CVE API

A simple FastAPI application to list CVEs (Common Vulnerabilities and Exposures), ingesting data from the National Vulnerability Database (NVD) and storing it in an SQLite database.

## Features

*   **CVE Data Ingestion:** Fetches and stores CVE data from the NVD API.
*   **API Endpoint:** Provides a RESTful API endpoint to list CVEs with various query parameters for filtering, sorting, and pagination.

## Setup

### Prerequisites

*   Python 3.8+

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
    (Note: Replace `<repository-url>` and `<repository-directory>` with actual values if known, otherwise assume current directory)

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Ingesting CVE Data

Before running the API, you need to ingest some CVE data into the SQLite database. This can be done by running the `db.py` script directly:

```bash
python db.py
```
This will create a `data.db` file in the project directory and populate it with initial CVE data from the NVD.

### Running the API

Start the FastAPI application using Uvicorn:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading upon code changes during development.

### API Endpoint

**`GET /list_cve`**

Lists CVEs with optional filtering, sorting, and pagination.

**Query Parameters:**

*   `cve_id` (string, optional): Filter by a specific CVE ID (e.g., `CVE-2023-1234`).
*   `order_by_date` (boolean, optional): If `true`, sort CVEs by published date in descending order. Defaults to `false`.
*   `page` (integer, optional): The page number for pagination. Defaults to `1`.
*   `limit` (integer, optional): The number of results per page. Minimum `10`, maximum `100`. Defaults to `20`.

**Example Request:**

```
GET http://127.0.0.1:8000/list_cve?order_by_date=true&page=1&limit=50
```

## Testing

Tests are located in `test.py`. To run them, you would typically use a test runner. (Further instructions on running tests will be added if a specific test framework is used).

To run the `test.py` file simply run:
```
python test.py
```