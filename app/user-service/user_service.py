import psycopg2
from flask import Flask, Response, jsonify, request

from database import count_users, create_user, ensure_schema, get_connection, list_users, serialize_row


app = Flask(__name__)


@app.get("/api/users")
def users_index():
    try:
        users = [serialize_row(user) for user in list_users()]
        return jsonify(service="user-service", users=users)
    except psycopg2.Error:
        app.logger.exception("Could not fetch users")
        return jsonify(error="database unavailable"), 503


@app.post("/api/users")
def users_create():
    payload = request.get_json(silent=True) or {}
    display_name = str(payload.get("display_name", "")).strip()[:80]

    if not display_name:
        return jsonify(error="display_name is required"), 400

    try:
        user = serialize_row(create_user(display_name))
        return jsonify(service="user-service", user=user), 201
    except psycopg2.Error:
        app.logger.exception("Could not create user")
        return jsonify(error="database unavailable"), 503


@app.get("/api/users/stats")
def users_stats():
    try:
        return jsonify(service="user-service", user_count=count_users())
    except psycopg2.Error:
        app.logger.exception("Could not count users")
        return jsonify(error="database unavailable"), 503


@app.get("/healthz")
def healthz():
    return jsonify(service="user-service", status="ok")


@app.get("/readyz")
def readyz():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return jsonify(service="user-service", status="ready")
    except psycopg2.Error:
        return jsonify(service="user-service", status="not-ready"), 503


@app.get("/metrics")
def metrics():
    database_available = 1
    user_count = 0

    try:
        user_count = count_users()
    except psycopg2.Error:
        database_available = 0

    body = "\n".join(
        [
            "# HELP message_board_service_info Service process information.",
            "# TYPE message_board_service_info gauge",
            'message_board_service_info{service="user-service"} 1',
            "# HELP message_board_database_available Database readiness status.",
            "# TYPE message_board_database_available gauge",
            f'message_board_database_available{{service="user-service"}} {database_available}',
            "# HELP message_board_users_current Current user count.",
            "# TYPE message_board_users_current gauge",
            f'message_board_users_current{{service="user-service"}} {user_count}',
        ]
    )
    return Response(f"{body}\n", mimetype="text/plain; version=0.0.4")


ensure_schema()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
