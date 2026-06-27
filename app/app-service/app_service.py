import psycopg2
from flask import Flask, Response, jsonify, request

from database import (
    count_messages,
    create_message,
    delete_message,
    ensure_schema,
    get_connection,
    list_messages,
    serialize_row,
)


app = Flask(__name__)


@app.get("/api/apps")
def apps_index():
    return jsonify(
        service="app-service",
        routes=[
            "GET /api/apps/messages",
            "POST /api/apps/messages",
            "DELETE /api/apps/messages/<id>",
            "GET /api/apps/stats",
        ],
    )


@app.get("/api/apps/messages")
def messages_index():
    try:
        messages = [serialize_row(message) for message in list_messages()]
        return jsonify(service="app-service", messages=messages)
    except psycopg2.Error:
        app.logger.exception("Could not fetch messages")
        return jsonify(error="database unavailable"), 503


@app.post("/api/apps/messages")
def messages_create():
    payload = request.get_json(silent=True) or {}
    author = str(payload.get("author", "")).strip()[:60]
    body = str(payload.get("body", "")).strip()[:500]

    if not author or not body:
        return jsonify(error="author and body are required"), 400

    try:
        create_message(author, body)
        return jsonify(service="app-service", status="created"), 201
    except psycopg2.Error:
        app.logger.exception("Could not create message")
        return jsonify(error="database unavailable"), 503


@app.delete("/api/apps/messages/<int:message_id>")
def messages_delete(message_id):
    try:
        delete_message(message_id)
        return jsonify(service="app-service", status="deleted")
    except psycopg2.Error:
        app.logger.exception("Could not delete message")
        return jsonify(error="database unavailable"), 503


@app.get("/api/apps/stats")
def messages_stats():
    try:
        return jsonify(service="app-service", message_count=count_messages())
    except psycopg2.Error:
        app.logger.exception("Could not count messages")
        return jsonify(error="database unavailable"), 503


@app.get("/healthz")
def healthz():
    return jsonify(service="app-service", status="ok")


@app.get("/readyz")
def readyz():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return jsonify(service="app-service", status="ready")
    except psycopg2.Error:
        return jsonify(service="app-service", status="not-ready"), 503


@app.get("/metrics")
def metrics():
    database_available = 1
    message_count = 0

    try:
        message_count = count_messages()
    except psycopg2.Error:
        database_available = 0

    body = "\n".join(
        [
            "# HELP message_board_service_info Service process information.",
            "# TYPE message_board_service_info gauge",
            'message_board_service_info{service="app-service"} 1',
            "# HELP message_board_database_available Database readiness status.",
            "# TYPE message_board_database_available gauge",
            f'message_board_database_available{{service="app-service"}} {database_available}',
            "# HELP message_board_messages_current Current message count.",
            "# TYPE message_board_messages_current gauge",
            f'message_board_messages_current{{service="app-service"}} {message_count}',
        ]
    )
    return Response(f"{body}\n", mimetype="text/plain; version=0.0.4")


ensure_schema()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
