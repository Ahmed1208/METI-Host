import datetime
import re
import os
import csv
from flask import Flask, render_template, request, session, redirect, jsonify
from flask_cors import CORS
import yaml
from version import get_version_from_github


app = Flask(__name__)
CORS(app)
# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key-change-this')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin-delete')


def tier1(input_text):
    # Example processing logic — replace with your actual logic
    return f"Processed: {input_text.upper()} ahmed.hossam1"


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    return request.remote_addr


def format_timestamp(timestamp_str):
    """Convert ISO timestamp to a more readable format"""
    try:
        dt = datetime.datetime.fromisoformat(timestamp_str)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp_str


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    name = session.get("username")
    show_delete_form = False

    if request.method == "POST":
        if not name:
            name = request.form.get("username")
            if name:
                session["username"] = name

        user_input = request.form["user_input"]
        ip = get_client_ip()
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.datetime.now().isoformat()

        with open("user_inputs.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}\t{name}\t{ip}\t{user_agent}\t{user_input}\n")

        session["last_result"] = tier1(user_input)

        return redirect(request.path)

    # Retrieve result after redirect
    result = session.pop("last_result", "")

    messages = []
    try:
        with open("user_inputs.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip('\n').split('\t', 4)
                if len(parts) == 5:
                    timestamp, _, _, _, message = parts
                    indent = "\n" + " " * 11
                    # Convert \n to indent
                    unescaped_msg = message.replace("\\n", indent)

                    # Convert URLs into hyperlinks
                    url_pattern = re.compile(r"(https?://[^\s]+)")
                    unescaped_msg = re.sub(url_pattern, r"<a href='\1' target='_blank'>\1</a>", unescaped_msg)

                    if unescaped_msg.strip():
                        formatted_timestamp = format_timestamp(timestamp)
                        delete_button = ""

                        formatted_msg = (
                            "<div class='message-container' style='white-space: pre-wrap; margin-bottom: 10px; position: relative;'>"
                            "<span style='color:blue;'>Anonymous:</span> "
                            f"{unescaped_msg}{delete_button}"
                            f"<div class='timestamp-tooltip' style='display: none; position: absolute; background: rgba(0,0,0,0.8); color: white; padding: 5px 8px; border-radius: 4px; font-size: 12px; top: -35px; left: 0; white-space: nowrap; z-index: 1000;'>{formatted_timestamp}</div>"
                            "</div>"
                        )

                        messages.append(formatted_msg)
        messages.reverse()
    except FileNotFoundError:
        messages = []

    return render_template("index.html", result=result, name=name,
                           all_messages="<br>".join(messages),
                           show_delete_form=show_delete_form)


@app.route("/amin-delete", methods=["GET", "POST"])
def admin_delete():
    # Check if admin is already authenticated
    if not session.get("admin_authenticated"):
        if request.method == "POST":
            password = request.form.get("admin_password", "")
            if password == ADMIN_PASSWORD:
                session["admin_authenticated"] = True
                return redirect("/amin-delete")
            else:
                # Wrong password, redirect to home
                return redirect("/")
        else:
            # Show password form
            return render_template("admin_login.html")

    # Admin is authenticated, show delete interface
    result = ""
    name = session.get("username")
    show_delete_form = True

    if request.method == "POST":
        if not name:
            name = request.form.get("username")
            if name:
                session["username"] = name

        user_input = request.form["user_input"]
        ip = get_client_ip()
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.datetime.now().isoformat()

        with open("user_inputs.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}\t{name}\t{ip}\t{user_agent}\t{user_input}\n")

        session["last_result"] = tier1(user_input)

        return redirect(request.path)

    # Retrieve result after redirect
    result = session.pop("last_result", "")

    messages = []
    try:
        with open("user_inputs.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip('\n').split('\t', 4)
                if len(parts) == 5:
                    timestamp, _, _, _, message = parts
                    indent = "\n" + " " * 11
                    # Convert \n to indent
                    unescaped_msg = message.replace("\\n", indent)

                    # Convert URLs into hyperlinks
                    url_pattern = re.compile(r"(https?://[^\s]+)")
                    unescaped_msg = re.sub(url_pattern, r"<a href='\1' target='_blank'>\1</a>", unescaped_msg)

                    if unescaped_msg.strip():
                        formatted_timestamp = format_timestamp(timestamp)
                        delete_button = ""
                        if show_delete_form:
                            delete_button = (
                                f"<form method='post' action='/delete_message' "
                                f"onsubmit='return confirm(\"Are you sure you want to delete this message?\");' "
                                f"style='display:inline;'>"
                                f"<input type='hidden' name='message_text' value='{message}'>"
                                f"<button type='submit' style='margin-left:10px; color:red;'>🗑️</button>"
                                f"</form>"
                            )

                        formatted_msg = (
                            "<div class='message-container' style='white-space: pre-wrap; margin-bottom: 10px; position: relative;'>"
                            "<span style='color:blue;'>Anonymous:</span> "
                            f"{unescaped_msg}{delete_button}"
                            f"<div class='timestamp-tooltip' style='display: none; position: absolute; background: rgba(0,0,0,0.8); color: white; padding: 5px 8px; border-radius: 4px; font-size: 12px; top: -35px; left: 0; white-space: nowrap; z-index: 1000;'>{formatted_timestamp}</div>"
                            "</div>"
                        )

                        messages.append(formatted_msg)
        messages.reverse()
    except FileNotFoundError:
        messages = []

    return render_template("index.html", result=result, name=name,
                           all_messages="<br>".join(messages),
                           show_delete_form=show_delete_form)


@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_authenticated", None)
    return redirect("/")


@app.route("/version", methods=["POST"])
def get_version():  # This method Read the Current Config and return the Value of the Version.
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            return jsonify(config.get("version", "0.0.0"))
    except FileNotFoundError:
        return jsonify("0.0.0")  # Return a default version if the file doesn't exist


@app.route("/delete_message", methods=["POST"])
def delete_message():
    message_to_delete = request.form.get("message_text", "").strip()
    if not message_to_delete:
        return redirect(request.referrer or "/")

    try:
        with open("user_inputs.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Reverse loop to delete only the last exact match
        for i in reversed(range(len(lines))):
            parts = lines[i].rstrip('\n').split('\t', 4)
            if len(parts) == 5:
                _, _, _, _, message = parts
                if message.strip() == message_to_delete:
                    del lines[i]
                    break

        with open("user_inputs.txt", "w", encoding="utf-8") as f:
            f.writelines(lines)

    except FileNotFoundError:
        pass

    return redirect(request.referrer or "/")


@app.route("/get_messages")
def get_messages():
    messages = []
    try:
        with open("user_inputs.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip('\n').split('\t', 4)
                if len(parts) == 5:
                    timestamp, _, _, _, message = parts
                    indent = "\n" + " " * 11
                    # Convert \n to indent
                    unescaped_msg = message.replace("\\n", indent)

                    # Convert URLs into hyperlinks
                    url_pattern = re.compile(r"(https?://[^\s]+)")
                    unescaped_msg = re.sub(url_pattern, r"<a href='\1' target='_blank'>\1</a>", unescaped_msg)

                    if unescaped_msg.strip():
                        formatted_timestamp = format_timestamp(timestamp)
                        formatted_msg = (
                            "<div class='message-container' style='white-space: pre-wrap; margin-bottom: 10px; position: relative;'>"
                            "<span style='color:blue;'>Anonymous:</span> "
                            f"{unescaped_msg}"
                            f"<div class='timestamp-tooltip' style='display: none; position: absolute; background: rgba(0,0,0,0.8); color: white; padding: 5px 8px; border-radius: 4px; font-size: 12px; top: -35px; left: 0; white-space: nowrap; z-index: 1000;'>{formatted_timestamp}</div>"
                            "</div>"
                        )
                        messages.append(formatted_msg)
        messages.reverse()
    except FileNotFoundError:
        messages = []

    return "<br>".join(messages)


@app.route('/menus', methods=["POST"])
def get_menus():
    menus = []
    with open('menus.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            menus.append({
                "id": int(row['id']),
                "name": row['name'],
                "link": row['link'],
                "note": row['note']
            })
    return jsonify(menus)


# Add this function to make version available in templates
@app.context_processor
def inject_version():
    try:
        return {'app_version': get_version_from_github()}
    except Exception as e:
        print(f"Version error: {e}")
        return {'app_version': 'v1.0.0'}

# Optional: Add a simple test route to check version
@app.route('/test-version')
def test_version():
    return f"Version: {get_version_from_github()}"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
