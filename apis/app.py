
import os

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)
DATABASE_URL = os.getenv("DATABASE_URL")



def get_db():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


@app.route("/")
def home():
    return  jsonify({"message": "Welcome to the Delta State Election Results API"})


# Get Delta State LGAs
@app.route("/api/pull/results")
def get_results():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    polling_unit_uniqueid,
                    party_abbreviation,
                    party_score,entered_by_user,date_entered
                FROM announced_pu_results
            """)

            results = cur.fetchall()

    return jsonify(results)


@app.route("/api/lgas")
def get_lgas():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT lga_id, lga_name
                FROM lga
                ORDER BY lga_name
            """)

            lgas = cur.fetchall()

    return jsonify(lgas)

@app.route("/api/lga/results/<int:lga_id>")
def get_lga_results(lga_id):

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    apr.party_abbreviation,
                    SUM(apr.party_score) AS total_votes
                FROM announced_pu_results apr
                JOIN polling_unit pu
                    ON pu.uniqueid = apr.polling_unit_uniqueid::integer
                JOIN lga l
                    ON l.lga_id = pu.lga_id
                WHERE l.lga_id = %s
                GROUP BY apr.party_abbreviation
                ORDER BY total_votes DESC
            """, (lga_id,))

            results = cur.fetchall()

    return jsonify(results)



    data = request.get_json()

    polling_unit_id = data.get("polling_unit_uniqueid")
    results = data.get("results", [])

    if not polling_unit_id or not results:
        return jsonify({"error": "Polling unit and party results are required"}), 400

    with get_db() as conn:
        with conn.cursor() as cur:
            for result in results:
                cur.execute("""
                    INSERT INTO announced_pu_results (
                        polling_unit_uniqueid,
                        party_abbreviation,
                        party_score,
                        entered_by_user,
                        date_entered,
                        user_ip_address
                    )
                    VALUES (%s, %s, %s, %s, NOW(), %s)
                """, (
                    str(polling_unit_id),
                    result["party_abbreviation"],
                    result["party_score"],
                    data.get("entered_by_user", "admin"),
                    request.remote_addr
                ))

    return jsonify({
        "message": "Polling unit results saved successfully"
    }), 201




@app.route("/api/polling-units", methods=["GET"])
def get_polling_units():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT uniqueid, polling_unit_name
                FROM polling_unit
                ORDER BY polling_unit_name
            """)
            units = cur.fetchall()

    return jsonify(units)

@app.route("/api/parties", methods=["GET"])
def get_parties():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT partyname
                FROM party
                ORDER BY partyname
            """)
            parties = cur.fetchall()

    return jsonify(parties)

@app.route("/api/polling-unit/results", methods=["POST"])
def save_polling_unit_results():
    data = request.get_json()

    polling_unit_id = data.get("polling_unit_uniqueid")
    entered_by = data.get("entered_by_user")
    results = data.get("results", [])

    if not polling_unit_id or not entered_by or not results:
        return jsonify({"error": "All fields are required"}), 400

    with get_db() as conn:
        with conn.cursor() as cur:
            for result in results:
                cur.execute("""
                    INSERT INTO announced_pu_results (
                        polling_unit_uniqueid,
                        party_abbreviation,
                        party_score,
                        entered_by_user,
                        date_entered,
                        user_ip_address
                    )
                    VALUES (%s, %s, %s, %s, NOW(), %s)
                """, (
                    str(polling_unit_id),
                    result["party_abbreviation"],
                    result["party_score"],
                    entered_by,
                    request.remote_addr
                ))

    return jsonify({
        "message": "All party results saved successfully!"
    }), 201
if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT"))
