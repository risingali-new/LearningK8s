import os

import requests
from flask import Flask, Response, flash, jsonify, redirect, render_template, request, url_for


REQUEST_TIMEOUT = 3


def service_url(env_name, default):
    return os.getenv(env_name, default).rstrip("/")


def user_service_url():
    return service_url("USER_SERVICE_URL", "http://user-service:5001/api/users")


def app_service_url():
    return service_url("APP_SERVICE_URL", "http://app-service:5002/api/apps")


def user_service_health_url():
    return service_url("USER_SERVICE_HEALTH_URL", "http://user-service:5001/readyz")


def app_service_health_url():
    return service_url("APP_SERVICE_HEALTH_URL", "http://app-service:5002/readyz")


def fetch_messages():
    response = requests.get(f"{app_service_url()}/messages", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json().get("messages", [])


def fetch_stats():
    stats = {}

    user_response = requests.get(f"{user_service_url()}/stats", timeout=REQUEST_TIMEOUT)
    user_response.raise_for_status()
    stats.update(user_response.json())

    app_response = requests.get(f"{app_service_url()}/stats", timeout=REQUEST_TIMEOUT)
    app_response.raise_for_status()
    stats.update(app_response.json())

    return stats


def create_user(display_name):
    response = requests.post(
        user_service_url(),
        json={"display_name": display_name},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()


def create_message(author, body):
    response = requests.post(
        f"{app_service_url()}/messages",
        json={"author": author, "body": body},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()


def delete_message(message_id):
    response = requests.delete(
        f"{app_service_url()}/messages/{message_id}",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-me-for-real-use")


@app.template_filter("display_time")
def display_time(value):
    if not value:
        return ""
    return str(value).replace("T", " ").replace("+00:00", " UTC").split(".")[0]


@app.get("/")
def index():
    service_error = None
    messages = []
    stats = None

    try:
        messages = fetch_messages()
    except requests.RequestException as exc:
        app.logger.warning("Could not fetch messages from app-service: %s", exc)
        service_error = "App service is not available yet."

    try:
        stats = fetch_stats()
    except requests.RequestException as exc:
        app.logger.warning("Could not fetch stats from services: %s", exc)

    return render_template(
        "index.html",
        messages=messages,
        db_error=service_error,
        stats=stats,
    )


@app.post("/messages")
def add_message():
    author = request.form.get("author", "").strip()[:60]
    body = request.form.get("body", "").strip()[:500]

    if not author or not body:
        flash("Name and message are required.")
        return redirect(url_for("index"))

    try:
        create_user(author)
        create_message(author, body)
        flash("Message saved.")
    except requests.RequestException as exc:
        app.logger.warning("Could not save message through services: %s", exc)
        flash("Message could not be saved because a service is unavailable.")

    return redirect(url_for("index"))


@app.post("/messages/<int:message_id>/delete")
def remove_message(message_id):
    try:
        delete_message(message_id)
        flash("Message deleted.")
    except requests.RequestException as exc:
        app.logger.warning("Could not delete message through app-service: %s", exc)
        flash("Message could not be deleted because app-service is unavailable.")

    return redirect(url_for("index"))


@app.get("/healthz")
def healthz():
    return jsonify(service="frontend", status="ok")


@app.get("/readyz")
def readyz():
    try:
        requests.get(user_service_health_url(), timeout=REQUEST_TIMEOUT).raise_for_status()
        requests.get(app_service_health_url(), timeout=REQUEST_TIMEOUT).raise_for_status()
        return jsonify(service="frontend", status="ready")
    except requests.RequestException:
        return jsonify(service="frontend", status="not-ready"), 503


@app.get("/metrics")
def metrics():
    body = "\n".join(
        [
            "# HELP message_board_service_info Service process information.",
            "# TYPE message_board_service_info gauge",
            'message_board_service_info{service="frontend"} 1',
        ]
    )
    return Response(f"{body}\n", mimetype="text/plain; version=0.0.4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
