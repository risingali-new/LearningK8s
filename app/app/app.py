import os

import psycopg2
from flask import Flask, Response, flash, jsonify, redirect, render_template, request, url_for

from database import count_messages, create_message, delete_message, ensure_schema, get_connection, list_messages


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-me-for-real-use")


@app.template_filter("display_time")
def display_time(value):
    if not value:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return str(value).replace("T", " ").replace("+00:00", " UTC").split(".")[0]


@app.get("/")
def index():
    db_error = None
    messages = []

    try:
        messages = list_messages()
    except psycopg2.Error:
        app.logger.exception("Could not fetch messages")
        db_error = "Database is not available yet."

    return render_template("index.html", messages=messages, db_error=db_error, stats=None)


@app.post("/messages")
def add_message():
    author = request.form.get("author", "").strip()[:60]
    body = request.form.get("body", "").strip()[:500]

    if not author or not body:
        flash("Name and message are required.")
        return redirect(url_for("index"))

    try:
        create_message(author, body)
        flash("Message saved.")
    except psycopg2.Error:
        app.logger.exception("Could not save message")
        flash("Message could not be saved because the database is unavailable.")

    return redirect(url_for("index"))


@app.post("/messages/<int:message_id>/delete")
def remove_message(message_id):
    try:
        delete_message(message_id)
        flash("Message deleted.")
    except psycopg2.Error:
        app.logger.exception("Could not delete message")
        flash("Message could not be deleted because the database is unavailable.")

    return redirect(url_for("index"))


@app.get("/healthz")
def healthz():
    return jsonify(service="monolith", status="ok")


@app.get("/readyz")
def readyz():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return jsonify(service="monolith", status="ready")
    except psycopg2.Error:
        return jsonify(service="monolith", status="not-ready"), 503


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
            'message_board_service_info{service="monolith"} 1',
            "# HELP message_board_database_available Database readiness status.",
            "# TYPE message_board_database_available gauge",
            f'message_board_database_available{{service="monolith"}} {database_available}',
            "# HELP message_board_messages_current Current message count.",
            "# TYPE message_board_messages_current gauge",
            f'message_board_messages_current{{service="monolith"}} {message_count}',
        ]
    )
    return Response(f"{body}\n", mimetype="text/plain; version=0.0.4")


ensure_schema()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
