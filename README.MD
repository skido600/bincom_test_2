# Delta State Election Results

## Overview

This project gives election teams and officials a straightforward way to manage Delta State election results. Instead of juggling spreadsheets or paper records, users can view polling unit scores, see totals grouped by local government area, and enter new results through a clean web interface. It keeps all election data in one place so teams can track results quickly and accurately.

## System Architecture

```mermaid
flowchart LR
    WebClient["Web Client"]
    FlaskAPI["Flask API"]
    Database[("PostgreSQL")]

    WebClient -- "HTTP API" --> FlaskAPI
    FlaskAPI -- "SQL" --> Database

    style WebClient fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#fff
    style FlaskAPI fill:#2e1065,stroke:#8b5cf6,stroke-width:2px,color:#fff
    style Database fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff
```

## Features

- **Browse Polling Unit Results** - View all recorded party scores by polling unit in a responsive table.
- **Summarize by Local Government** - Select an LGA and instantly see vote totals per party.
- **Submit New Results** - Record scores for each party at any polling unit through a simple form.
- **Reference Data Lookup** - Load polling units and political parties dynamically from the backend.

### Viewing LGA Results

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API as Flask API
    participant DB as Database

    User->>Browser: Select LGA
    Browser->>API: GET /api/lga/results/:id
    API->>DB: Sum votes by party
    DB->>API: Return totals
    API->>Browser: JSON results
    Browser->>User: Display vote table
```

### Storing Polling Unit Results

```mermaid
sequenceDiagram
    actor Official
    participant Browser
    participant API as Flask API
    participant DB as Database

    Official->>Browser: Choose polling unit and enter scores
    Browser->>API: POST /api/polling-unit/results
    API->>DB: Insert result records
    DB->>API: Confirm save
    API->>Browser: Success response
    Browser->>Official: Show confirmation
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/skido600/bincom_test_2.git
cd bincom_test_2
```

2. Create and activate a Python virtual environment:

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install flask psycopg python-dotenv flask-cors
```

4. Create a `.env` file in the project root and add your PostgreSQL connection string:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/election_db
```

5. Start the Flask server:

```bash
python apis/app.py
```

6. Open the UI files in `ui/` with any static file server, or simply open `ui/index.html` in your browser.

## Usage

Once the server is running, the frontend pages connect to `http://localhost:5000` by default.

- Open `ui/index.html` to view all polling unit results.
- Open `ui/lga.html` to select a local government and see aggregated party totals.
- Open `ui/store-results.html` to choose a polling unit, enter scores for each party, and save them to the database.

## API Documentation

The API runs on `http://localhost:5000` and serves the following endpoints.

#### GET /api/pull/results

Returns all announced polling unit results.

**Request:**

None.

**Response:**

```json
[
  {
    "polling_unit_uniqueid": "1",
    "party_abbreviation": "PDP",
    "party_score": 124,
    "entered_by_user": "admin",
    "date_entered": "..."
  }
]
```

#### GET /api/lgas

Returns all local government areas ordered by name.

**Response:**

```json
[
  {
    "lga_id": 1,
    "lga_name": "Aniocha North"
  }
]
```

#### GET /api/lga/results/{lga_id}

Returns total votes per party for the selected local government area.

**Response:**

```json
[
  {
    "party_abbreviation": "PDP",
    "total_votes": 5000
  }
]
```

#### GET /api/polling-units

Returns all polling units ordered by name.

**Response:**

```json
[
  {
    "uniqueid": 1,
    "polling_unit_name": "Unit A"
  }
]
```

#### GET /api/parties

Returns all political parties ordered by name.

**Response:**

```json
[
  {
    "partyname": "PDP"
  }
]
```

#### POST /api/polling-unit/results

Saves party scores for a polling unit.

**Request:**

```json
{
  "polling_unit_uniqueid": "1",
  "entered_by_user": "john_doe",
  "results": [
    {
      "party_abbreviation": "PDP",
      "party_score": 150
    },
    {
      "party_abbreviation": "APC",
      "party_score": 89
    }
  ]
}
```

**Response:**

```json
{
  "message": "All party results saved successfully!"
}
```

**Errors:**

- `400 Bad Request` - Returned when `polling_unit_uniqueid`, `entered_by_user`, or `results` are missing or empty.

### Environment Variables

| Variable     | Description                     | Example                                      |
| ------------ | ------------------------------- | -------------------------------------------- |
| DATABASE_URL | PostgreSQL connection string.   | `postgresql://user:pass@localhost/election`  |

## Technologies Used

| Technology  | Description                                   |
| ----------- | --------------------------------------------- |
| Python      | Backend logic and API server.                 |
| Flask       | Lightweight web framework for routing.        |
| PostgreSQL  | Relational database for election data.          |
| HTML/CSS/JS | Frontend pages for viewing and entering data.  |
| psycopg     | Modern PostgreSQL driver for Python.          |
| Flask-CORS  | Enables cross-origin requests for the UI.     |

## Contributing

Contributions are welcome. If you would like to improve the project, fork the repository, create a feature branch, and open a pull request with a clear description of your changes.

## Author

- GitHub: [skido600](https://github.com/skido600)

## Badges

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://dokugen.samueltuoyo.com)