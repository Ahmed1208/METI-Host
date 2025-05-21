import datetime
import re
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with a secure, random key

def tier1(input_text):
    # Example processing logic — replace with your actual logic
    return f"Processed: {input_text.upper()} ahmed.hossam1"

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    return request.remote_addr

# @app.route("/", methods=["GET", "POST"])
# def home():
#     result = ""
#     name = session.get("username")
#
#     if request.method == "POST":
#         # Save username if not already in session
#         if not name:
#             name = request.form.get("username")
#             if name:
#                 session["username"] = name
#
#         user_input = request.form["user_input"]
#         ip = get_client_ip()
#         user_agent = request.headers.get('User-Agent')
#         timestamp = datetime.datetime.now().isoformat()
#
#         # Save all data to a file
#         with open("user_inputs.txt", "a", encoding="utf-8") as f:
#             f.write(f"{timestamp}\t{name}\t{ip}\t{user_agent}\t{user_input}\n")
#
#         result = tier1(user_input)
#
#     return render_template("index.html", result=result, name=name)

@app.route("/", methods=["GET", "POST"])
@app.route("/amin-delete", methods=["GET", "POST"])
def home():
    result = ""
    name = session.get("username")
    show_delete_form = request.path == "/amin-delete"

    if request.method == "POST":
        if not name:
            name = request.form.get("username")
            if name:
                session["username"] = name

        user_input = request.form["user_input"].strip()
        ip = get_client_ip()
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.datetime.now().isoformat()
        #Check if input is the keyword
        if user_input == "/demas":
            user_input = "Here is the Demas Menu: <a href='https://drive.google.com/file/d/1ZjTJNlRQEhO4eAhdAzZxbq2Z0xArc9rj/view?usp=drive_link'>Click Here</a>"

        # Log the input to the file
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
                    _, _, _, _, message = parts
                    indent = "\n" + " " * 11
                    unescaped_msg = message.replace("\\n", indent)
                    #Do not replace the urls to be hyperlinks if the input is the keyword 
                    if unescaped_msg != "Here is the Demas Menu: <a href='https://drive.google.com/file/d/1ZjTJNlRQEhO4eAhdAzZxbq2Z0xArc9rj/view?usp=drive_link'>Click Here</a>":
                        # Convert URLs into hyperlinks
                        url_pattern = re.compile(r"(https?://[^\s]+)")
                        unescaped_msg = re.sub(url_pattern, r"<a href='\1' target='_blank'>\1</a>", unescaped_msg)
                    if unescaped_msg.strip():
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
                            "<div style='white-space: pre-wrap; margin-bottom: 10px;'>"
                            "<span style='color:blue;'>Anonymous:</span> "
                            f"{unescaped_msg}{delete_button}</div>"
                        )

                        messages.append(formatted_msg)
        messages.reverse()
    except FileNotFoundError:
        messages = []

    return render_template("index.html", result=result, name=name,
                           all_messages="<br>".join(messages),
                           show_delete_form=show_delete_form)


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
                    _, _, _, _, message = parts
                    indent = "\n" + " " * 11
                    # Convert \n to indent
                    unescaped_msg = message.replace("\\n", indent)
                    #Do not replace the urls to be hyperlinks if the input is the keyword 
                    if unescaped_msg != "Here is the Demas Menu: <a href='https://drive.google.com/file/d/1ZjTJNlRQEhO4eAhdAzZxbq2Z0xArc9rj/view?usp=drive_link'>Click Here</a>":
                        # Convert URLs into hyperlinks
                        url_pattern = re.compile(r"(https?://[^\s]+)")
                        unescaped_msg = re.sub(url_pattern, r"<a href='\1' target='_blank'>\1</a>", unescaped_msg)

                    if unescaped_msg.strip():
                        formatted_msg = (
                            "<div style='white-space: pre-wrap; margin-bottom: 10px;'>"
                            "<span style='color:blue;'>Anonymous:</span> "
                            f"{unescaped_msg}</div>"
                        )
                        messages.append(formatted_msg)
        messages.reverse()
    except FileNotFoundError:
        messages = []

    return "<br>".join(messages)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
